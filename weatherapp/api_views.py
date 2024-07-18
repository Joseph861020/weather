from django.db.models import Count
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
from .models import CitySearchHistory
from .views import weather_view, autocomplete_city, search_history


@csrf_exempt
def city_search_count(request):
    """
    Возвращает количество поисков для каждого города в виде JSON.

    :param request: HttpRequest объект
    :return: JsonResponse с данными о количестве поисков для каждого города
    """
    data = list(CitySearchHistory.objects.values('city').annotate(count=Count('city')))
    return JsonResponse(data, safe=False)
