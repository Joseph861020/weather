import requests
from django.conf import settings


def get_weather(city: str) -> dict:
    """
    Получает данные о погоде для заданного города.

    :param city: Название города
    :return: Данные о погоде в формате JSON
    """
    # Используйте соответствующий сервис геокодирования для получения широты и долготы для города
    # Этот пример использует фиктивную функцию для простоты
    lat, lon = get_lat_lon_for_city(city)

    url = 'https://api.weather.yandex.ru/v2/forecast'
    headers = {
        'X-Yandex-API-Key': settings.YANDEX_API_KEY,
    }
    params = {
        'lat': lat,
        'lon': lon,
        'lang': 'en_US',
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        # Логируем ошибку и возвращаем пустой словарь в случае ошибки запроса
        logger.error(f"Ошибка при получении данных о погоде: {e}")
        return {}

    return response.json()


def get_lat_lon_for_city(city: str) -> tuple[float, float]:
    """
    Фиктивная функция для преобразования названия города в широту и долготу.
    Замените на реальный сервис геокодирования.

    :param city: Название города
    :return: Кортеж с широтой и долготой (lat, lon)
    """
    # В реальной реализации использовать API геокодирования, например, Google Maps или OpenStreetMap
    # Здесь возвращаем координаты для Амстердама как пример
    return 52.37125, 4.89388
