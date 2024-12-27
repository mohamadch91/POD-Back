from django.urls import path
from .views import *
from django.contrib import admin
from Order import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import *
urlpatterns = [

    path('admin/', admin.site.urls),
    path('detail/', OrderDetailView.as_view(), name='get detail of one order'),
    path('user-active/', UserOrderView.as_view(), name='get user orders'),
    path('add/', AddOrderView.as_view(), name='add order'),
    path('change-status/', ChangeStatusView.as_view(), name='change status of order'),
    path('list/admin', OrderViewAdmin.as_view(), name='change status of order'),
    

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)