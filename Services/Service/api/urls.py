from django.urls import path
from .views import *

urlpatterns = [
    path('list/', ServiceListView.as_view(), name='get all service'),
    path('detail/', ServiceDetailView.as_view(), name='get detail of one service'),
    path('user-active/', UserServiceView.as_view(), name='get user services'),
    path('add/', AddServiceView.as_view(), name='add service'),
    path('delete/', DeleteServiceView.as_view(), name='delete service'),
    path('edit/', EditServiceView.as_view(), name='edit  service'),


]