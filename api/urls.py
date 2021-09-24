from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import StoreWeatherInfo, ListWeatherInfo

router = DefaultRouter()
router.register('weather', ListWeatherInfo)

urlpatterns = [
    path('weather/store/', StoreWeatherInfo.as_view(), name='storeweather'),
    path('', include(router.urls))
]
