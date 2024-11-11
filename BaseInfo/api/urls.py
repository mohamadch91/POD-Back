from django.urls import path
from .views import *
from django.contrib import admin

urlpatterns = [
    path('provinces/', ProvinceView.as_view(), name='get all provinces'),
    path('cities/', CityView.as_view(), name='get all cities'),
    path('commerceBrands/', CommerceBrandsView.as_view(), name='get all cities'),
    path('commerCategories/', CommerceCategoryView.as_view(), name='get all cities'),
    path('serviceBrands/', ServiceBrandsView.as_view(), name='get all cities'),
    path('serviceCategories/', ServiceCategoryView.as_view(), name='get all cities'),
    path('saleMethods/', SaleMethodsView.as_view(), name='get all cities'),
    path('deliveryMethods/', DeliveryMethodsView.as_view(), name='get all cities'),


    path('admin/', admin.site.urls),

 


    
    


]