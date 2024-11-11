
from rest_framework import serializers
from .models import *

  

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
class SaleMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleMethod
        fields = '__all__'

class DeliveryMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryMethod
        fields = '__all__'
