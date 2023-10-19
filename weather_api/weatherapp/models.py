from django.db import models

# Create your models here.
class WeatherForecast(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    forecast_type = models.CharField(max_length=100)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_data_fresh(self):
        import datetime
        now = datetime.datetime.now(datetime.timezone.utc)
        elapsed_time = now - self.created_at
        # return elapsed_time.total_seconds() < 60  # 10 minutes in seconds
        return elapsed_time.total_seconds() < 600  # 10 minutes in seconds
