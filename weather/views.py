from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.core.cache import cache
from .models import OverriddenForecast
from .serializers import ForecastOverrideSerializer
from .services.weatherapi import WeatherAPIService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

city_param = openapi.Parameter(
    'city', openapi.IN_QUERY, description="Название города на английском языке", type=openapi.TYPE_STRING,
    required=True
)

date_param = openapi.Parameter(
    'date', openapi.IN_QUERY, description='Дата в формате "dd.MM.yyyy"', type=openapi.TYPE_STRING,
    required=True
)


class CurrentWeatherView(APIView):

    @swagger_auto_schema(
        operation_description="Возвращает текущую температуру и локальное время в указанном городе.",
        manual_parameters=[city_param],
        responses={
            200: openapi.Response(
                description="Успешный ответ с температурой и локальным временем",
                examples={
                    "application/json": {
                        "temperature": 22.1,
                        "local_time": "16:45"
                    }
                }
            ),
            400: 'Город не найден или параметр city отсутствует'
        }
    )

    def get(self, request):
        city = request.query_params.get("city")
        if not city:
            return Response({"error": "Missing 'city' query parameter"}, status=400)

        cache_key = f"current_weather_{city.lower()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        try:
            service = WeatherAPIService()
            data = service.get_current_weather(city)
            cache.set(cache_key, data, timeout=600)
            return Response(data)
        except ValueError as e:
            return Response({"error": str(e)}, status=404)


class ForecastWeatherView(APIView):

    @swagger_auto_schema(
        operation_description="Возвращает прогноз температуры (мин. и макс.) на заданную дату для города.",
        manual_parameters=[city_param, date_param],
        responses={
            200: openapi.Response(
                description="Успешный ответ с минимальной и максимальной температурой",
                examples={
                    "application/json": {
                        "min_temperature": 11.1,
                        "max_temperature": 24.5
                    }
                }
            ),
            400: 'Ошибка валидации (например, неверный формат даты или дата вне допустимого диапазона)',
            404: 'Город не найден'
        }
    )

    def get(self, request):
        city = request.query_params.get("city")
        date_str = request.query_params.get("date")

        if not city or not date_str:
            return Response({"error": "Missing 'city' or 'date' query parameter"}, status=400)

        try:
            date = datetime.strptime(date_str, "%d.%m.%Y").date()
            if date < datetime.today().date():
                return Response({"error": "Date cannot be in the past"}, status=400)
            if date > (datetime.today().date() + timedelta(days=10)):
                return Response({"error": "Date cannot be more than 10 days in the future"}, status=400)

            forecast = OverriddenForecast.objects.filter(city=city, date=date).first()
            if forecast:
                return Response({
                    "min_temperature": forecast.min_temperature,
                    "max_temperature": forecast.max_temperature
                })

            cache_key = f"forecast_{city.lower()}_{date_str}"
            cached_forecast = cache.get(cache_key)
            if cached_forecast:
                return Response(cached_forecast)

            service = WeatherAPIService()
            forecast_data = service.get_forecast(city, date_str)
            cache.set(cache_key, forecast_data, timeout=600)
            return Response(forecast_data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)


    @swagger_auto_schema(
        operation_description="Задает или переопределяет прогноз погоды для указанного города и даты.",
        request_body=ForecastOverrideSerializer,
        responses={
            200: 'Данные успешно сохранены',
            400: 'Ошибка валидации данных',
        }
    )
    def post(self, request):
        serializer = ForecastOverrideSerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.validated_data["city"].lower()
            date = serializer.validated_data["date"].strftime("%d.%m.%Y")

            instance, _ = OverriddenForecast.objects.update_or_create(
                city=serializer.validated_data["city"],
                date=serializer.validated_data["date"],
                defaults={
                    "min_temperature": serializer.validated_data["min_temperature"],
                    "max_temperature": serializer.validated_data["max_temperature"]
                }
            )
            cache_key = f"forecast_{city}_{date}"
            cache.delete(cache_key)

            return Response(serializer.data)
        return Response(serializer.errors, status=400)
