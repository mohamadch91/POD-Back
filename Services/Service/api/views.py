import http
from re import L
from django.shortcuts import render

# Create your views here.
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permissions import auth

class ProvinceView(generics.ListAPIView):
    queryset =Province.objects.all()
    def get(self, request):
        Provinces = Province.objects.all()
        serializer = ProvinceSerializer(Provinces,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CityView(generics.ListAPIView):
    queryset =City.objects.all()
 
    def get(self, request):
        prov = request.query_params["id"]
        cities = City.objects.filter( province = prov)
        serializer = CitySerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
