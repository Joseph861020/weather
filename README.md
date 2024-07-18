# Приложение для Прогноза Погоды

## Описание

Это Django-приложение позволяет пользователям получать текущий прогноз погоды для выбранного города. Приложение также сохраняет историю поиска городов для каждого пользователя.

## Функции

- Получение текущего прогноза погоды по выбранному городу.
- Сохранение истории поиска городов.
- Автозаполнение названий городов.

## Установка

### Использование Docker

1. Убедитесь, что у вас установлены [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).

2. Клонируйте репозиторий:
    ```sh
    git clone(https://github.com/Joseph861020/weather.git)
    cd weatherapp
    ```

3. Создайте файл `.env` и добавьте необходимые переменные окружения:
    ```env
    DEBUG=True
    YANDEX_WEATHER_API_KEY=YOUR_YANDEX_WEATHER_API_KEY
    DATABASE_URL=postgres://user:password@db:5432/weatherapp
    ```

4. Соберите и запустите контейнеры Docker:
    ```sh
    docker-compose up --build
    ```

5. Выполните миграции базы данных и создайте суперпользователя:
    ```sh
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

6. Откройте приложение в браузере по адресу [http://localhost:8000](http://localhost:8000).

### Локальная установка

1. Убедитесь, что у вас установлены Python 3.10 и PostgreSQL.

2. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/Joseph861020/weather.git
    cd weatherapp
    ```

3. Создайте виртуальное окружение и активируйте его:
    ```sh
    python -m venv venv
    source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
    ```

4. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

5. Создайте файл `.env` и добавьте необходимые переменные окружения:
    ```env
    DEBUG=True
    DATABASE_URL=postgres://user:password@localhost:5432/weatherapp
    YANDEX_WEATHER_API_KEY=YOUR_YANDEX_WEATHER_API_KEY
    ```

6. Выполните миграции базы данных и создайте суперпользователя:
    ```sh
    python manage.py migrate
    python manage.py createsuperuser
    ```

7. Запустите сервер разработки:
    ```sh
    python manage.py runserver
    ```

8. Откройте приложение в браузере по адресу [http://localhost:8000](http://localhost:8000).

## Тестирование

Для запуска тестов используйте следующую команду:

```sh
docker-compose exec web python manage.py test
```
## Структура проекта
* weatherapp/: Основное приложение Django.
* Dockerfile: Инструкция по созданию Docker-образа.
* docker-compose.yml: Конфигурация Docker Compose.
* requirements.txt: Список зависимостей Python.
* README.md: Этот файл.
## Используемые технологии
* Django
* Docker
* PostgreSQL
* API прогноза погоды


### Объяснение

1. **Описание и Функции**: Краткое описание и перечисление основных возможностей приложения.
    - **Описание**: Приложение для получения текущего прогноза погоды по выбранному городу.
    - **Функции**: Получение прогноза погоды, сохранение истории поиска, автозаполнение названий городов.

2. **Установка**: Инструкции по установке с использованием Docker и без него.
    - **Docker**: Установка Docker и Docker Compose, клонирование репозитория, настройка переменных окружения, сборка и запуск контейнеров, миграции базы данных, создание суперпользователя, запуск приложения.
    - **Локальная установка**: Установка Python 3.10 и PostgreSQL, клонирование репозитория, создание виртуального окружения, установка зависимостей, настройка переменных окружения, миграции базы данных, создание суперпользователя, запуск сервера разработки.

3. **Тестирование**: Команда для запуска тестов.
    - **Команда**: `docker-compose exec web python manage.py test`

4. **Структура проекта**: Описание основных директорий и файлов в проекте.
    - **weatherapp/**: Основное приложение Django.
    - **Dockerfile**: Инструкция по созданию Docker-образа.
    - **docker-compose.yml**: Конфигурация Docker Compose.
    - **requirements.txt**: Список зависимостей Python.
    - **README.md**: Этот файл.

5. **Используемые технологии**: Перечисление технологий, использованных в проекте.
    - **Технологии**: Django, Docker, PostgreSQL, API прогноза погоды.

6. **Авторы и Лицензия**: Информация об авторах и лицензии проекта.
    - **Авторы**: [Джозеф](https://github.com/Joseph861020).
    - **Лицензия**: MIT License.

Этот README предоставляет полную информацию для начала работы с приложением и его установки.
