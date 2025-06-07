from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import OverriddenForecast

class ForecastOverrideSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=["%d.%m.%Y"])

    class Meta:
        model = OverriddenForecast
        fields = '__all__'

    def validate(self, data):
        today = timezone.now().date()

        if data['min_temperature'] > data['max_temperature']:
            raise serializers.ValidationError("min_temperature cannot be greater than max_temperature")

        if data['date'] < today:
            raise serializers.ValidationError("Date cannot be in the past")

        if data['date'] > today + timedelta(days=10):
            raise serializers.ValidationError("Date cannot be more than 10 days in the future")

        return data
