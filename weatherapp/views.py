import logging

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets

from .forms import CityForm
from .models import CitySearchHistory
from .serializers import CitySearchHistorySerializer

logger = logging.getLogger(__name__)


@login_required
def weather_view(request):
    """
    Представление для отображения погоды и сохранения истории поиска.

    :param request: HttpRequest объект
    :return: HttpResponse объект
    """
    form = CityForm()
    context = {'form': form, 'weather_data': None, 'error_message': None}

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather(city)

            if weather_data:
                save_search_history(request.user, city)
                context['city'] = city
                context['weather_data'] = weather_data
            else:
                context['error_message'] = 'Данные о погоде для этого города недоступны.'

    # Retrieve user's search history
    history = CitySearchHistory.objects.filter(user=request.user).order_by('-timestamp')[:5]
    context['search_history'] = history

    return render(request, 'index.html', context)


def save_search_history(user, city):
    """
    Сохранение истории поиска города для пользователя.

    :param user: пользователь (User объект)
    :param city: город (строка)
    """
    try:
        history, created = CitySearchHistory.objects.get_or_create(user=user, city=city)
        if not created:
            history.timestamp = timezone.now()  # Обновляем временную метку, если запись уже существует
            history.save()
    except Exception as e:
        logger.error(f"Ошибка сохранения истории поиска: {e}")


def get_weather(city):
    """
    Получение данных о погоде для заданного города.

    :param city: город (строка)
    :return: данные о погоде (словарь) или None, если данные недоступны
    """
    url = f'https://api.weather.yandex.ru/v2/forecast'
    params = {'city': city, 'lang': 'en_US'}
    headers = {'X-Yandex-Weather-Key': settings.YANDEX_WEATHER_API_KEY}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        weather_data = response.json()
        logger.info(f"Full weather data for {city}: {weather_data}")

        if 'forecasts' in weather_data:
            forecast_hours = weather_data['forecasts'][0]['hours'][:2]  # Get next 2 hours forecast
            logger.info(f"Hourly weather data for {city}: {forecast_hours}")
            return forecast_hours
        else:
            logger.warning(f"Incomplete weather data for {city}: {weather_data}")
            return None  # Обработка случая, когда данные о погоде неполные или недоступны

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка получения данных о погоде для города '{city}': {e}")
        return None


@login_required
def search_history(request):
    """
    Представление для отображения истории поиска пользователя.

    :param request: HttpRequest объект
    :return: HttpResponse объект с историей поиска
    """
    history = CitySearchHistory.objects.filter(user=request.user)
    return render(request, 'history.html', {'history': history})


class CitySearchHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с историей поиска городов через REST API.
    """
    queryset = CitySearchHistory.objects.all()
    serializer_class = CitySearchHistorySerializer


def autocomplete_city(request):
    """
    Автозаполнение поля ввода города на основе истории поиска.

    :param request: HttpRequest объект
    :return: JsonResponse с массивом городов
    """
    if 'term' in request.GET:
        term = request.GET['term']
        cities = CitySearchHistory.objects.filter(city__icontains=term).values_list('city', flat=True).distinct()
        return JsonResponse(list(cities), safe=False)
    return JsonResponse([], safe=False)
