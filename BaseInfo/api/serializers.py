from dataclasses import field, fields
from os import access
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.hashers import make_password



  

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'
        
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','value','province']
        
class CommerceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CommerceCategory
        fields = '__all__'
class ServiceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceCategory
        fields = '__all__'
class CommerceBrandsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommerceBrands
        fields = '__all__'
class ServiceBrandsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceBrands
        fields = '__all__'
