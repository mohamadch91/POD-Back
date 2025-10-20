from django.urls import path
from .views import *
from django.contrib import admin
from Search import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import *
urlpatterns = [

    path('admin/', admin.site.urls),
     path('', SearchView.as_view(), name='get all commerce'),


]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)