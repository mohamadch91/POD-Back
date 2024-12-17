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
    

class CommerceBrandsAdminView(APIView):


    def get(self, request):
        commerceBrands = CommerceBrands.objects.all()
        serializer = CommerceBrandsSerializer(commerceBrands,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CommerceBrandsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        commerceBrand = get_object_or_404(CommerceBrands, id=request.data["id"])
        serializer = CommerceBrandsSerializer(commerceBrand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        id = request.GET.get('id')
        commerceBrand = get_object_or_404(CommerceBrands, id = id)
        commerceBrand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommerceCategoryAdminView(APIView):


    def get(self, request):
        commerceCategories = CommerceCategory.objects.all()
        serializer = CommerceCategorySerializer(commerceCategories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CommerceCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        commerceCategory = get_object_or_404(CommerceCategory, id=request.data["id"])
        serializer = CommerceCategorySerializer(commerceCategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        id = request.GET.get('id')
        commerceCategory = get_object_or_404(CommerceCategory, id = id)
        commerceCategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ServiceBrandsAdminView(APIView):
    
        def get(self, request):
            serviceBrands = ServiceBrands.objects.all()
            serializer = ServiceBrandsSerializer(serviceBrands,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        def post(self, request):
            serializer = ServiceBrandsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def put(self, request):
            serviceBrand = get_object_or_404(ServiceBrands, id=request.data["id"])
            serializer = ServiceBrandsSerializer(serviceBrand, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def delete(self, request):
            id = request.GET.get('id')
            serviceBrand = get_object_or_404(ServiceBrands, id = id)
            serviceBrand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class ServiceCategoryAdminView(APIView):
        
            def get(self, request):
                serviceCategories = ServiceCategory.objects.all()
                serializer = ServiceCategorySerializer(serviceCategories,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            
            def post(self, request):
                serializer = ServiceCategorySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            def put(self, request):
                serviceCategory = get_object_or_404(ServiceCategory, id=request.data["id"])
                serializer = ServiceCategorySerializer(serviceCategory, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            def delete(self, request):
                id = request.GET.get('id')
                serviceCategory = get_object_or_404(ServiceCategory, id = id)
                serviceCategory.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            

class SaleMethodsAdminView(APIView):
        
        def get(self, request):
            saleMethods = SaleMethod.objects.all()
            serializer = SaleMethodSerializer(saleMethods,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        def post(self, request):
            serializer = SaleMethodSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def put(self, request):
            saleMethod = get_object_or_404(SaleMethod, id=request.data["id"])
            serializer = SaleMethodSerializer(saleMethod, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def delete(self, request):
            id = request.GET.get('id')
            saleMethod = get_object_or_404(SaleMethod, id = id)
            saleMethod.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        

class DeliveryMethodsAdminView(APIView):
    
        def get(self, request):
            deliveryMethods = DeliveryMethod.objects.all()
            serializer = DeliveryMethodSerializer(deliveryMethods,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        def post(self, request):
            serializer = DeliveryMethodSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def put(self, request):
            deliveryMethod = get_object_or_404(DeliveryMethod, id=request.data["id"])
            serializer = DeliveryMethodSerializer(deliveryMethod, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def delete(self, request):
            id = request.GET.get('id')
            deliveryMethod = get_object_or_404(DeliveryMethod, id = id)
            deliveryMethod.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class CommerceStatusAdminView(APIView):
    
        def get(self, request):
            commerceStatus = CommerceStatus.objects.all()
            serializer = CommerceStatusSerializer(commerceStatus,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        def post(self, request):
            serializer = CommerceStatusSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def put(self, request):
            commerceStatus = get_object_or_404(CommerceStatus, id=request.data["id"])
            serializer = CommerceStatusSerializer(commerceStatus, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def delete(self, request):
            id = request.GET.get('id')
            commerceStatus = get_object_or_404(CommerceStatus, id = id)
            commerceStatus.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
class ServiceStatusAdminView(APIView):

        def get(self, request):
            serviceStatus = ServiceStatus.objects.all()
            serializer = ServiceStatusSerializer(serviceStatus,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        def post(self, request):
            serializer = ServiceStatusSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def put(self, request):
            serviceStatus = get_object_or_404(ServiceStatus, id=request.data["id"])
            serializer = ServiceStatusSerializer(serviceStatus, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def delete(self, request):
            id = request.GET.get('id')
            serviceStatus = get_object_or_404(ServiceStatus, id = id)
            serviceStatus.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class ActivityTypeAdminView(APIView):
    
        def get(self, request):
            activityTypes = ActivityType.objects.all()
            serializer = ActivityTypeSerializer(activityTypes,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        def post(self, request):
            serializer = ActivityTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def put(self, request):
            activityType = get_object_or_404(ActivityType, id=request.data["id"])
            serializer = ActivityTypeSerializer(activityType, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def delete(self, request):
            id = request.GET.get('id')
            activityType = get_object_or_404(ActivityType, id = id)
            activityType.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class BusinessTypeAdminView(APIView):
        
            def get(self, request):
                businessTypes = BusinessVariety.objects.all()
                serializer = BusinessVarietySerializer(businessTypes,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            
            def post(self, request):
                serializer = BusinessVarietySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            def put(self, request):
                businessType = get_object_or_404(BusinessVariety, id=request.data["id"])
                serializer = BusinessVarietySerializer(businessType, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            def delete(self, request):
                id = request.GET.get('id')
                businessType = get_object_or_404(BusinessVariety, id = id)
                businessType.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            

class OrderStatusAdminView(APIView):
    
        def get(self, request):
            orderStatuses = OrderStatus.objects.all()
            serializer = OrderStatusSerializer(orderStatuses,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        def post(self, request):
            serializer = OrderStatusSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def put(self, request):
            orderStatus = get_object_or_404(OrderStatus, id=request.data["id"])
            serializer = OrderStatusSerializer(orderStatus, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        def delete(self, request):
            id = request.GET.get('id')
            orderStatus = get_object_or_404(OrderStatus, id = id)
            orderStatus.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)