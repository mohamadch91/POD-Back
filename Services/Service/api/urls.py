from django.urls import path
from .views import *

urlpatterns = [
    path('list/', ProvinceView.as_view(), name='get all provinces'),
    path('detail/', ProvinceView.as_view(), name='get all provinces'),
    path('user-active/', CityView.as_view(), name='get all cities'),
    path('add/', CityView.as_view(), name='get all cities'),
    path('delet/', CityView.as_view(), name='get all cities'),
    path('edit/', CityView.as_view(), name='get all cities'),


]