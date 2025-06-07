from django.urls import path
from .views import CurrentWeatherView, ForecastWeatherView

urlpatterns = [
    path('api/weather/current', CurrentWeatherView.as_view()),
    path('api/weather/forecast', ForecastWeatherView.as_view()),
]
