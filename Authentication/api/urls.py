from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView,TokenVerifyView


urlpatterns = [
  
    # path('sregister/', StudentRegisterView.as_view(), name='auth_register'),
    # path('tregister/', TeacherRegisterView.as_view(), name='auth_register'),
    # path('uregister/',UserRegisterView.as_view(),name="user register"),
    # path('users/', UserListView.as_view(), name='user_list'),
    path('update_profile/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('sms/login/',OTPViewLogin.as_view(),name="OTP view login"),
    path('sms/register/',OTPViewRegister.as_view(),name="OTP viewvregister "),
    path('delete/',deleteUser.as_view(),name="delete user"),
    path('user/', UserView.as_view(), name='admin_login'),
    path('legal/', LegalUserView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='profile'),


    # path('currupted/', CurruptedView.as_view(), name='currupted'),
    # path('login_to_user/', loginUserView.as_view(), name='l user'),
    # path('user_ip/', UseripView.as_view(), name='l user'),


    
    


]