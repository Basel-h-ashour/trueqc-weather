from django.http.response import HttpResponse, JsonResponse
import requests

from django.shortcuts import render
from rest_framework import generics

from .serializers import WeatherInputSerializer, WeatherDataSerializer


class StoreWeatherInfo(generics.CreateAPIView):
    serializer_class = WeatherInputSerializer

    def create(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        url = ( 'https://api.openweathermap.org/data/2.5/weather?lat='
                f'{latitude}&lon={longitude}&appid='
                '1b62fa92aeb084d60f61307d2458d5e7')
        
        response = requests.get(url)

        
        if response.status_code == 200:
            weather_json = response.json()

            weather_data_serializer = WeatherDataSerializer(
                data={
                'location_name': weather_json.get('name'),
                'weather_main': weather_json.get('weather')[0].get('main'),
                'weather_desc': weather_json.get('weather')[0]\
                                .get('description'),
                'temp': weather_json.get('main').get('temp'),
                'pressure': weather_json.get('main').get('pressure'),
                'humidity': weather_json.get('main').get('humidity'),
                'visibility': weather_json.get('visibility'),
                'wind_speed': weather_json.get('wind').get('speed'),
            })

            if weather_data_serializer.is_valid():
                weather_data_serializer.save()
        else:
            return HttpResponse(status=400)