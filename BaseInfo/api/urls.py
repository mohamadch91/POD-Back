from django.urls import path
from .views import *
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import *
from BaseInfo import settings
urlpatterns = [
    path('provinces/', ProvinceView.as_view(), name='get all provinces'),
    path('cities/', CityView.as_view(), name='get all cities'),
    path('countries/', CityView.as_view(), name='get all cities'),
    path('countryAdmin/', CityView.as_view(), name='get all cities'),

    path('commerceBrands/', CommerceBrandsView.as_view(), name='get all cities'),
    path('commerCategories/', CommerceCategoryView.as_view(), name='get all cities'),
    path('serviceBrands/', ServiceBrandsView.as_view(), name='get all cities'),
    path('serviceCategories/', ServiceCategoryView.as_view(), name='get all cities'),
    path('saleMethods/', SaleMethodsView.as_view(), name='get all cities'),
    path('deliveryMethods/', DeliveryMethodsView.as_view(), name='get all cities'),
    path('commerceStatus/', CommerceStatusView.as_view(), name='get all cities'),
    path('serviceStatus/', ServiceStatusView.as_view(), name='get all cities'),
    path('activityTypes/', ActivityTypeView.as_view(), name='get all cities'),
    path('businessVariety/', BusinessTypeView.as_view(), name='get all cities'),
    # admin panel API's
    path('commerceBrandsAdmin/', CommerceBrandsAdminView.as_view(), name='get all cities'),
    path('commerCategoriesAdmin/', CommerceCategoryAdminView.as_view(), name='get all cities'),
    path('serviceBrandsAdmin/', ServiceBrandsAdminView.as_view(), name='get all cities'),
    path('serviceCategoriesAdmin/', ServiceCategoryAdminView.as_view(), name='get all cities'),
    path('saleMethodsAdmin/', SaleMethodsAdminView.as_view(), name='get all cities'),
    path('deliveryMethodsAdmin/', DeliveryMethodsAdminView.as_view(), name='get all cities'),
    path('commerceStatusAdmin/', CommerceStatusAdminView.as_view(), name='get all cities'),
    path('serviceStatusAdmin/', ServiceStatusAdminView.as_view(), name='get all cities'),
    path('activityTypesAdmin/', ActivityTypeAdminView.as_view(), name='get all cities'),
    path('businessVarietyAdmin/', BusinessTypeAdminView.as_view(), name='get all cities'),
    path('orderStatusAdmin/', OrderStatusAdminView.as_view(), name='get all cities'),



    path('admin/', admin.site.urls),



]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

