from django.urls import path
from .views import *
from django.contrib import admin
from logs import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import *
urlpatterns = [
    path('permium/', PermiumRequestView.as_view(), name='get all commerce'),
    path('consultation/', ConsultationRequestView.as_view(), name='get all commerce'),
    path('admin/permium/', PermiumRequestAdminView.as_view(), name='get all commerce'),
    path('admin/consultation/', ConsultationRequestAdminView.as_view(), name='get all commerce'),
    path('contact-us/', ContactUsView.as_view(), name='get all commerce'),
    path('admin/contact-us//', ContactUsAdminView.as_view(), name='get all commerce'),
    

    path('admin/', admin.site.urls),


]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)