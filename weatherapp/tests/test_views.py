import unittest
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User
from django.test import RequestFactory

from weatherapp.views import weather_view, save_search_history, get_weather


class WeatherViewTestCase(unittest.TestCase):
    """
    Тесты для проверки функционала взаимодействия с погодным приложением.
    """

    def setUp(self) -> None:
        """
        Подготовка данных для каждого теста.
        """
        self.factory: RequestFactory = RequestFactory()
        self.user: User = User.objects.create_user(username='testuser', password='password')

    def tearDown(self) -> None:
        """
        Очистка данных после каждого теста.
        """
        self.user.delete()

    @patch('weatherapp.views.CityForm')
    @patch('weatherapp.views.get_weather')
    @patch('weatherapp.views.CitySearchHistory.objects.get_or_create')
    def test_weather_view_post_valid_form(self, mock_get_or_create: MagicMock, mock_get_weather: MagicMock,
                                          MockCityForm: MagicMock) -> None:
        """
        Проверка поведения представления weather_view при отправке корректной формы.
        """
        mock_form_instance = MockCityForm.return_value
        mock_form_instance.is_valid.return_value = True
        mock_form_instance.cleaned_data = {'city': 'Moscow'}

        mock_get_weather.return_value = [
            {'hour': '0', 'temp': 16, 'condition': 'cloudy', 'humidity': 87, 'wind_speed': 1.3, 'wind_dir': 'w'},
            {'hour': '1', 'temp': 16, 'condition': 'cloudy', 'humidity': 87, 'wind_speed': 1.3, 'wind_dir': 'w'}
        ]

        mock_history_instance = MagicMock()
        mock_get_or_create.return_value = (mock_history_instance, False)

        request = self.factory.post('/', {'city': 'Moscow'})
        request.user = self.user

        response = weather_view(request)

        self.assertEqual(response.status_code, 200)
        mock_get_or_create.assert_called_once()

    @patch('weatherapp.views.CityForm')
    @patch('weatherapp.views.get_weather')
    @patch('weatherapp.views.CitySearchHistory.objects.get_or_create')
    def test_weather_view_post_invalid_form(self, mock_get_or_create: MagicMock, mock_get_weather: MagicMock,
                                            MockCityForm: MagicMock) -> None:
        """
        Проверка поведения представления weather_view при отправке некорректной формы.
        """
        mock_form_instance = MockCityForm.return_value
        mock_form_instance.is_valid.return_value = False

        request = self.factory.post('/', {'city': 'Invalid City'})
        request.user = self.user

        response = weather_view(request)

        self.assertEqual(response.status_code, 200)
        mock_get_or_create.assert_not_called()

    @patch('weatherapp.views.CitySearchHistory.objects.get_or_create')
    def test_save_search_history(self, mock_get_or_create: MagicMock) -> None:
        """
        Проверка функции сохранения истории поиска.
        """
        mock_history_instance = MagicMock()
        mock_get_or_create.return_value = (mock_history_instance, False)

        save_search_history(self.user, 'Moscow')

        mock_get_or_create.assert_called_once_with(user=self.user, city='Moscow')

    @patch('weatherapp.views.requests.get')
    def test_get_weather_success(self, mock_requests_get: MagicMock) -> None:
        """
        Проверка функции получения погодных данных при успешном запросе.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'forecasts': [
                {'hours': [
                    {'hour': '0', 'temp': 20, 'condition': 'sunny', 'humidity': 50, 'wind_speed': 3, 'wind_dir': 'SE'},
                    {'hour': '1', 'temp': 21, 'condition': 'sunny', 'humidity': 45, 'wind_speed': 3, 'wind_dir': 'SE'}
                ]}
            ]
        }
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        weather_data = get_weather('Moscow')

        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data[0]['temp'], 20)
        self.assertEqual(weather_data[0]['condition'], 'sunny')

    @patch('weatherapp.views.requests.get')
    def test_get_weather_failure(self, mock_requests_get: MagicMock) -> None:
        """
        Проверка функции получения погодных данных при неудачном запросе.
        """
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        weather_data = get_weather('InvalidCity')

        self.assertIsNone(weather_data)


if __name__ == '__main__':
    unittest.main()
