from django.urls import path

from .api_views import city_search_count
from .views import weather_view, autocomplete_city, CitySearchHistoryViewSet, search_history

urlpatterns = [
    path('', weather_view, name='weather_view'),
    path('autocomplete_city/', autocomplete_city, name='autocomplete_city'),
    path('history/', search_history, name='search_history'),
    path('api/city_search_count/', CitySearchHistoryViewSet.as_view({'get': 'list'}), name='city_search_count'),
    path('api/city_search_count/', city_search_count, name='city_search_count')
]
