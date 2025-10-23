from django.urls import path
from .views import *
from rest_framework_simplejwt.views import  TokenObtainPairView
from django.contrib import admin
from authentication import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import *

urlpatterns = [
  
   
    path('update_profile/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('sms/login/',OTPViewLogin.as_view(),name="OTP view login"),
    path('sms/login/admin/',OTPViewLoginAdmin.as_view(),name="OTP view login"),
    path('sms/register/',OTPViewRegister.as_view(),name="OTP viewvregister "),
    path('delete/',deleteUser.as_view(),name="delete user"),
    path('user/', UserView.as_view(), name='admin_login'),
    path('legal/', LegalUserView.as_view(), name='profile'),
    path('real/', RealUserView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='profile'),
    path('user-admin/', UserAdminView.as_view(), name='profile'),
    path('user/status/', UserStatusView.as_view(), name='profile'),
    path('sms/admin/',OTPViewAdmin.as_view(),name="OTP viewvregister "),
    path('admin/', admin.site.urls),



]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)