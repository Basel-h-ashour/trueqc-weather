from django.urls import path

from .views import StoreWeatherInfo

urlpatterns = [
    path('weather/store/', StoreWeatherInfo.as_view(), name='storeweather')
]
