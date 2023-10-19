from django.shortcuts import render
import requests
from rest_framework.generics import *
from .models import WeatherForecast
from .serializers import WeatherForecastSerializer
from rest_framework.response import Response
from django.utils import timezone

# Create your views here.
class WeatherForecastRetriveCreateAPIView(ListCreateAPIView):
    queryset = WeatherForecast.objects.all()
    serializer_class = WeatherForecastSerializer

    FORECAST_TYPE_MAPPING = {
        'current': {'type': 'current', 'exclude': 'hourly,daily'},
        'minutely': {'type': 'current', 'exclude': 'hourly,daily'},
        'hourly': {'type': 'current', 'exclude': 'hourly,daily,minutely'},
        '48 hourly': {'type': 'hourly', 'exclude': 'current,daily,minutely'},
        '48hourly': {'type': 'hourly', 'exclude': 'current,daily,minutely'},
        'daily': {'type': 'daily', 'exclude': 'current,hourly,minutely'},
        '7daily': {'type': '7daily', 'exclude': 'current,hourly,minutely'},
        '7 daily': {'type': '7 daily', 'exclude': 'current,hourly,minutely'},

    }

    def get_queryset(self):
        data = self.request.data
        lat = data.get('lat')
        lon = data.get('lon')
        forecast_type = data.get('type')

        forecast_type_mapping = self.FORECAST_TYPE_MAPPING.get(forecast_type)

        if forecast_type_mapping:
            try:
                # Check if the data is available in the local DB and fresh
                weather_forecast = WeatherForecast.objects.get(lat=lat, lon=lon, forecast_type=forecast_type)
                if weather_forecast.is_data_fresh():
                    print("Data is coming from the database")
                    return WeatherForecast.objects.filter(lat=lat, lon=lon, forecast_type=forecast_type)
                else:
                    # Data is no longer fresh, update it with new data
                    api_url = 'https://api.openweathermap.org/data/2.5/onecall'
                    params = {
                        'lat': lat,
                        'lon': lon,
                        'type': forecast_type_mapping['type'],
                        'exclude': forecast_type_mapping['exclude'],
                        'appid': 'b0c49ca78c4f1de0fd0c4d05bedf3553'  # Replace with your openweathermap API key
                    }
                    response = requests.get(api_url, params=params)
                    new_data = response.json()

                    # Update the existing weather forecast with the new data
                    weather_forecast.data = new_data
                    weather_forecast.created_in = timezone.now()  # Use timezone.now() to get aware datetime
                    weather_forecast.save()

                    print("Data is updated without deleting")

                    return WeatherForecast.objects.filter(lat=lat, lon=lon, forecast_type=forecast_type)
            except WeatherForecast.DoesNotExist:
                pass

            # Request data from openweathermap and save it to the local DB
            api_url = 'https://api.openweathermap.org/data/2.5/onecall'
            params = {
                'lat': lat,
                'lon': lon,
                'type': forecast_type_mapping['type'],
                'exclude': forecast_type_mapping['exclude'],
                'appid': 'b0c49ca78c4f1de0fd0c4d05bedf3553'  # Replace with your openweathermap API key
            }
            response = requests.get(api_url, params=params)
            data = response.json()

            # Save the data to the local DB
            weather_forecast = WeatherForecast.objects.create(lat=lat, lon=lon, forecast_type=forecast_type, data=data)
            print("Data is coming from the API")

            return [weather_forecast]
        else:
            # Handle invalid forecast type
            print("Invalid forecast type")
            return []
        

    