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
        cities = CommerceCategory.objects.all()
        serializer = CommerceCategorySerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class ServiceCategoryView(generics.ListAPIView):
    queryset =ServiceCategory.objects.all()
 
    def get(self, request):
        cities = ServiceCategory.objects.all()
        serializer = ServiceCategorySerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class CommerceBrandsView(generics.ListAPIView):
    queryset =CommerceBrands.objects.all()
 
    def get(self, request):
        cities = CommerceBrands.objects.all()
        serializer = CommerceBrandsSerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class ServiceBrandsView(generics.ListAPIView):
    queryset =ServiceBrands.objects.all()
 
    def get(self, request):
        cities = ServiceBrands.objects.all()
        serializer = ServiceBrandsSerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class SaleMethodsView(generics.ListAPIView):
    queryset =SaleMethod.objects.all()
 
    def get(self, request):
        cities = SaleMethod.objects.all()
        serializer = SaleMethodSerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class DeliveryMethodsView(generics.ListAPIView):
    queryset =SaleMethod.objects.all()
 
    def get(self, request):
        cities = DeliveryMethod.objects.all()
        serializer = DeliveryMethodSerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class CommerceStatusView(generics.ListAPIView):
    queryset =CommerceStatus.objects.all()
 
    def get(self, request):
        cities = CommerceStatus.objects.all()
        serializer = CommerceStatusSerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ServiceStatusView(generics.ListAPIView):
    queryset =ServiceStatus.objects.all()
 
    def get(self, request):
        cities = ServiceStatus.objects.all()
        serializer = ServiceStatusSerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ActivityTypeView(generics.ListAPIView):
    queryset =ActivityType.objects.all()
 
    def get(self, request):
        cities = ActivityType.objects.all()
        serializer = ActivityTypeSerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class BusinessTypeView(generics.ListAPIView):
    queryset =BusinessVariety.objects.all()
 
    def get(self, request):
        cities = BusinessVariety.objects.all()
        serializer = BusinessVarietySerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class OrderStatusView(generics.ListAPIView):
    queryset =OrderStatus.objects.all()
 
    def get(self, request):
        cities = OrderStatus.objects.all()
        serializer = OrderStatusSerializer(cities,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)