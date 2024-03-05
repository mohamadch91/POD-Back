from django.urls import path
from .views import *

urlpatterns = [
    path('list/', CommerceListView.as_view(), name='get all commerce'),
    path('detail/', CommerceDetailView.as_view(), name='get detail of one commerce'),
    path('user-active/', UserCommerceView.as_view(), name='get user commerces'),
    path('add/', AddCommerceView.as_view(), name='add commerce'),
    path('delete/', DeleteCommerceView.as_view(), name='delete commerce'),
    path('edit/', EditCommerceView.as_view(), name='edit  commerce'),


]