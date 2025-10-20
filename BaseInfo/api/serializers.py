
from rest_framework import serializers
from .models import *
from django_grpc_framework import proto_serializers
import base_info_pb2
from google.protobuf.json_format import MessageToDict


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'
        
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','value','province']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        
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

class CommerceStatusSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = CommerceStatus
            fields = '__all__'

class ServiceStatusSerializer(serializers.ModelSerializer):
            class Meta:
                model = ServiceStatus
                fields = '__all__'


class ActivityTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityType
        fields = '__all__'

class BusinessVarietySerializer(serializers.ModelSerializer):
         
        class Meta:
            model = BusinessVariety
            fields = '__all__'

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'


class BaseInfoProtoSerializer(proto_serializers.ProtoSerializer):
    key = serializers.CharField()
    value = serializers.CharField()
    class Meta:
        proto_class = base_info_pb2.BaseInfoRequest
        fields = ['name', 'id']
    def message_to_data(self, message):
        """Protobuf message -> Dict of python primitive datatypes.
        """
        return MessageToDict(message)


class BaseInfoRequestProtoSerializer(proto_serializers.ProtoSerializer):
    baseInfo =serializers.ListField(child=BaseInfoProtoSerializer())
    class Meta:
        proto_class = base_info_pb2.GetBaseInfoResponse
        fields = '__all__'
    def message_to_data(self, message):
        """Protobuf message -> Dict of python primitive datatypes.
        """
        return MessageToDict(message)
       