from dataclasses import field, fields
from os import access
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.hashers import make_password



  

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        
class ServiceImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImages
        fields = '__all__'
        
        
class ServiceCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceComments
        fields = '__all__'
class ServiceVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceVotes
        fields = '__all__'
       