# 🌦️ Forecast API

REST API-сервис для получения текущей погоды и прогноза на ближайшие дни по городам. Реализовано с использованием **Django REST Framework** и внешнего API **WeatherAPI.com**.

---

## 🚀 Возможности

- Получение **текущей температуры и локального времени** по городу
- Получение **прогноза погоды** (мин/макс температура) на заданную дату
- **Переопределение прогноза** вручную через POST-запрос
- **Swagger-документация** (`/swagger/`)
- Кэширование внешних запросов
- Валидация данных и обработка ошибок

---

## 📎 Используемые технологии

  - Python 3.11+

  - Django 4.x

  - Django REST Framework

  - WeatherAPI.com

  - drf-yasg (Swagger)

  - SQLite (можно заменить)

---

## Структура проекта
<pre>
forecastapi/
├── forecastapi/             # Основной каталог проекта Django
│   ├── __init__.py
│   ├── settings.py          # Настройки проекта
│   ├── urls.py              # Главный маршрутизатор URL
│   └── wsgi.py              # Точка входа для WSGI-серверов
│
├── weather/                 # Приложение Django для обработки погодных данных
│   ├── __init__.py
│   ├── admin.py          
│   ├── apps.py          
│   ├── models.py            # Определение моделей данных
│   ├── serializers.py       # Сериализаторы для преобразования данных
│   ├── services/
│   │   └── weatherapi.py    # Взаимодействие с внешним API погоды
│   ├── tests.py             
│   └── views.py             # Обработчики запросов API
│
├── manage.py                # Утилита командной строки для управления проектом
├── requirements.txt         # Файл с зависимостями проекта
└── README.md                # Описание проекта
</pre>
---

## 📌 Примеры запросов
<pre>
GET /api/weather/current?city=London

{
  "temperature": 21.3,
  "local_time": "15:24"
}

GET /api/weather/forecast?city=Paris&date=11.06.2025

{
  "min_temperature": 12.5,
  "max_temperature": 22.8
}

POST /api/weather/forecast

{
  "city": "Berlin",
  "date": "11.06.2025",
  "min_temperature": 10.0,
  "max_temperature": 18.5
}
</pre>
---

## 🔧 Установка и запуск

1. Клонировать репозиторий

      ```bash
      git clone https://github.com/Stuspushka/forecastapi
      cd forecastapi

2. Установить зависимости

      ```bash
      python -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt

4. Настроить .env

      Создай файл .env на основе .env.template:
      
          cp .env.template .env
      
      Впиши свой ключ от WeatherAPI.com в переменную WEATHERAPI_KEY.

5. Применить миграции и запустить сервер

      ```bash
      python manage.py makemigrations
      python manage.py migrate
      python manage.py runserver

## 🧪 Swagger-документация

После запуска сервера Swagger доступен по адресу:

http://localhost:8000/swagger/
