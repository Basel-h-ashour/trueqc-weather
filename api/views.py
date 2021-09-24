import requests

from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import action
from rest_framework import generics, status, filters, viewsets, mixins
from rest_framework.response import Response

from .utils import queryset_to_workbook
from .models import WeatherData
from .serializers import WeatherInputSerializer, WeatherDataSerializer


class StoreWeatherInfo(generics.CreateAPIView):
    serializer_class = WeatherInputSerializer

    def create(self, request):
        lat = request.data.get('latitude')
        lon = request.data.get('longitude')
        url = ( 'https://api.openweathermap.org/data/2.5/weather?lat='
                f'{lat}&lon={lon}&appid='
                '1b62fa92aeb084d60f61307d2458d5e7')
        
        response = requests.get(url)

        
        if response.status_code == 200:
            weather_json = response.json()

            normalized_json = {
                'location_name': weather_json.get('name'),
                'weather_main': weather_json.get('weather')[0].get('main'),
                'weather_desc': weather_json.get('weather')[0]
                                .get('description'),
                'temp': weather_json.get('main').get('temp'),
                'pressure': weather_json.get('main').get('pressure'),
                'humidity': weather_json.get('main').get('humidity'),
                'visibility': weather_json.get('visibility'),
                'wind_speed': weather_json.get('wind').get('speed'),
            }

            weather_data_serializer = WeatherDataSerializer(
                data=normalized_json)

            weather_data_serializer.is_valid(raise_exception=True)
            weather_data_serializer.save()
            headers = self.get_success_headers(weather_data_serializer
                .data)

            return Response(data=normalized_json,
                    status=status.HTTP_201_CREATED, headers=headers)

        else:
            return Response({'response': ('The provided coordinates were '
                'invalid.')},
            status=status.HTTP_400_BAD_REQUEST)


class ListWeatherInfo(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = WeatherDataSerializer
    queryset = WeatherData.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('location_name', 'weather_main', 'weather_desc',)

    def get_queryset(self):
        """filters float ranges"""
        queryset = self.queryset

        temp_low = self.request.query_params.get('temp_low')
        temp_high = self.request.query_params.get('temp_high')
        pressure_low = self.request.query_params.get('pressure_low')
        pressure_high = self.request.query_params.get('pressure_high')
        humidity_low = self.request.query_params.get('humidity_low')
        humidity_high = self.request.query_params.get('humidity_high')
        visibility_low = self.request.query_params.get('visibility_low')
        visibility_high = self.request.query_params.get('visibility_high')
        wind_low = self.request.query_params.get('wind_low')
        wind_high = self.request.query_params.get('wind_high')

        if temp_low:
            queryset = queryset.filter(temp__gte=temp_low)
        if temp_high:
            queryset = queryset.filter(temp__lte=temp_high)
        if pressure_low:
            queryset = queryset.filter(pressure__gte=pressure_low)
        if pressure_high:
            queryset = queryset.filter(temp__lte=pressure_high)
        if humidity_low:
            queryset = queryset.filter(humidity__gte=humidity_low)
        if humidity_high:
            queryset = queryset.filter(humidity__lte=humidity_high)
        if visibility_low:
            queryset = queryset.filter(visibility__gte=visibility_low)
        if visibility_high:
            queryset = queryset.filter(visibility__lte=visibility_high)
        if wind_low:
            queryset = queryset.filter(wind_speed__gte=wind_low)
        if wind_high:
            queryset = queryset.filter(wind_speed__lte=wind_high)

        return queryset

    @action(methods=['GET'], detail=False, url_path='export')
    def export_results(self, request):
        queryset = self.get_queryset()

        columns = (
            'location_name',
            'weather_main',
            'weather_desc',
            'temp',
            'pressure',
            'humidity',
            'visibility',
            'wind_speed')

        workbook = queryset_to_workbook(queryset, columns)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Weather.xls"'
        workbook.save(response)
        return response      
