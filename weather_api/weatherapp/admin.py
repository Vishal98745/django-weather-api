from django.contrib import admin

# Register your models here.
from .models import *


class WeatherAdmin(admin.ModelAdmin):
    list_display = ['id', 'lat', 'lon', 'forecast_type', 'data', 'created_at']

admin.site.register(WeatherForecast, WeatherAdmin)
