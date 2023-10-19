
from django.urls import path
from .views import *
urlpatterns = [
    path('weather/', WeatherForecastRetriveCreateAPIView.as_view(), name='weather'),
]