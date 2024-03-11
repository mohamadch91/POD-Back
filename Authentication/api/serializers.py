from dataclasses import field, fields
from os import access
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','phone','birth','national_code','city','Province','postalCode','address','created_at','updated_at','picture']
    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)   
       
class LegalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalUser
        fields = ['pk','phone','birth','national_code','city','Province','postalCode','address','created_at','updated_at','picture','companyName','companyID','companyTitle']
    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)   

class RealUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealUser
        fields = ['pk','phone','birth','national_code','city','Province','postalCode','address','created_at','updated_at','picture','gender','first_name','last_name']
    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)   
         

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalUser
        fields = ['pk','birth','national_code','city','Province','postalCode','address','created_at','updated_at','picture']

class UpdateLegalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalUser
        fields = ['pk','birth','national_code','city','Province','postalCode','address','created_at','updated_at','picture','companyName','companyID','companyTitle']

class UpdateRealUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealUser
        fields = ['pk','phone','birth','national_code','city','Province','postalCode','address','created_at','updated_at','picture','gender','first_name','last_name']


class requestOTPSerializer(serializers.Serializer):
    reciever=serializers.IntegerField(allow_null=False)
        
class RequestOTPSerializer(serializers.Serializer):
    receiver = serializers.CharField( allow_null=False)


class RequestOTPResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields =['request_id']

class VerifyOtpRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(allow_null=False)
    password = serializers.CharField(allow_null=False)
    receiver = serializers.CharField( allow_null=False)

class ObtainTokenSerializer(serializers.Serializer):
    access = serializers.CharField( allow_null=False)
    refresh = serializers.CharField( allow_null=False)
    created = serializers.BooleanField()

class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model =Wallet
        fields = '__all__'

# class VerifyOtpResponseSuccesSerializer(serializers.Serializer):
#       login_data = ObtainTokenSerializer,
#       user_data = UserSerializer

# class userIpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = userIp
#         fields = '__all__'
