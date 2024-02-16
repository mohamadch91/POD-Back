from dataclasses import field, fields
from os import access
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.hashers import make_password



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['pk','phone','birth','national_code','role','first_name','last_name','created_at','updated_at','picture']
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
        

class updateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalUser
        fields = ['pk','phone','grade','department','birth','national_code','role','first_name','last_name','created_at','updated_at','picture','gpaverage','disipcline','school','parentName','parentNationalCode','pbirthday','peducation','pjob','address']

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

# class userIpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = userIp
#         fields = '__all__'
