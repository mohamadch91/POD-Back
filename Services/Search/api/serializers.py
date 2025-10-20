from dataclasses import field, fields
from os import access
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.hashers import make_password



  

class SearchResponseSerializer(serializers.ModelSerializer):
    name= serializers.CharField()
    image = serializers.CharField()
    type = models.CharField()
