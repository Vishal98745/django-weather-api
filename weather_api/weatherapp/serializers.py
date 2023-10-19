from rest_framework import serializers
from .models import WeatherForecast

class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = ['lat', 'lon', 'forecast_type', 'data', 'created_at']
