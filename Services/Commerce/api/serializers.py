from dataclasses import field, fields
from os import access
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.hashers import make_password



  

class CommerceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commerce
        fields = '__all__'
        
class CommerceImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommerceImages
        fields = '__all__'
        
class CommerceCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommerceComments
        fields = '__all__'
class CommerceVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommerceVotes
        fields = '__all__'
       