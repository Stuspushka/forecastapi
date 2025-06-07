import requests
from datetime import datetime
from django.conf import settings


class WeatherAPIService:
    BASE_URL = "http://api.weatherapi.com/v1"

    def __init__(self):
        self.api_key = settings.WEATHERAPI_KEY

    def get_current_weather(self, city):
        url = f"{self.BASE_URL}/current.json"
        params = {"key": self.api_key, "q": city}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ValueError("City not found or external API error.")
        data = response.json()
        return {
            "temperature": data["current"]["temp_c"],
            "local_time": data["location"]["localtime"].split(" ")[1]
        }

    def get_forecast(self, city, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Expected dd.MM.yyyy")
        url = f"{self.BASE_URL}/forecast.json"
        params = {"key": self.api_key, "q": city, "dt": date_obj.strftime("%Y-%m-%d")}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ValueError("City not found or forecast not available.")
        data = response.json()
        day = data.get("forecast", {}).get("forecastday", [])[0]["day"]
        return {
            "min_temperature": day["mintemp_c"],
            "max_temperature": day["maxtemp_c"]
        }
