import http
from re import L
from django.shortcuts import render

# Create your views here.
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.shortcuts import get_object_or_404
from itertools import chain


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
class CommerceCategoryView(generics.ListAPIView):
    queryset =CommerceCategory.objects.all()
 
    def get(self, request):
        prov = request.query_params["id"]
        cities = CommerceCategory.objects.filter( province = prov)
        serializer = CommerceCategorySerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class ServiceCategoryView(generics.ListAPIView):
    queryset =ServiceCategory.objects.all()
 
    def get(self, request):
        prov = request.query_params["id"]
        cities = ServiceCategory.objects.filter( province = prov)
        serializer = ServiceCategorySerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class CommerceBrands(generics.ListAPIView):
    queryset =CommerceBrands.objects.all()
 
    def get(self, request):
        prov = request.query_params["id"]
        cities = CommerceBrands.objects.filter( province = prov)
        serializer = CommerceBrandsSerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class ServiceBrandsView(generics.ListAPIView):
    queryset =ServiceBrands.objects.all()
 
    def get(self, request):
        prov = request.query_params["id"]
        cities = ServiceBrands.objects.filter( province = prov)
        serializer = ServiceBrandsSerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
