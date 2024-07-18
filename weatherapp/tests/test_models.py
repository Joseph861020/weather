from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase

from weatherapp.models import CitySearchHistory


class CitySearchHistoryModelTestCase(TestCase):
    """
    Тесты для модели CitySearchHistory.
    """

    def setUp(self):
        """
        Подготовка данных для каждого теста.
        """
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_city_search_history_creation(self):
        """
        Проверка создания записи истории поиска города.
        """
        # Создаем объект истории поиска города
        city_search = CitySearchHistory.objects.create(user=self.user, city='New York', count=1)

        # Проверяем строковое представление объекта
        self.assertEqual(str(city_search), 'testuser searched for New York 1 times')

    def test_unique_together_constraint(self):
        """
        Проверка уникального ограничения на пару (user, city).
        """
        # Создаем запись истории поиска города с одним пользователем и одним городом
        CitySearchHistory.objects.create(user=self.user, city='New York', count=1)

        # Пытаемся создать еще одну запись с тем же пользователем и городом
        with self.assertRaises(IntegrityError):
            CitySearchHistory.objects.create(user=self.user, city='New York', count=1)

    def test_last_searched_auto_now(self):
        """
        Проверка автоматического обновления времени последнего поиска.
        """
        # Создаем объект истории поиска города
        city_search = CitySearchHistory.objects.create(user=self.user, city='Los Angeles', count=1)

        # Получаем начальное значение last_searched
        initial_last_searched = city_search.last_searched

        # Симулируем еще один поиск через некоторое время (задержка в 1 секунду для демонстрации)
        city_search.save()
        city_search.refresh_from_db()
        city_search.timestamp = datetime.now() - timedelta(seconds=1)
        city_search.save()

        # Убеждаемся, что last_searched обновилось автоматически
        self.assertNotEqual(city_search.last_searched, initial_last_searched)
