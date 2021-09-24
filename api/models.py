from django.db import models


class WeatherData(models.Model):
    """database model lat&lon weather data"""
    class Meta:
        verbose_name_plural = 'Weather Data'

    location_name = models.CharField(max_length=255)
    weather_main = models.CharField(max_length=50)
    weather_desc = models.CharField(max_length=255)
    temp = models.FloatField()
    pressure = models.FloatField()
    humidity = models.FloatField()
    visibility = models.FloatField()
    wind_speed = models.FloatField()

    def __str__(self):
        return self.location_name