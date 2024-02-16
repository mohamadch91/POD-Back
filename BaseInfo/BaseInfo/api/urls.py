from django.urls import path
from .views import *

urlpatterns = [
    path('provinces/', ProvinceView.as_view(), name='get all provinces'),
    path('cities/', CityView.as_view(), name='get all cities'),
 


    
    


]