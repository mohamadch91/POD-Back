from dataclasses import field, fields
from os import access
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from django_grpc_framework import proto_serializers
import service_pb2
from google.protobuf.json_format import MessageToDict



  

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        
class ServiceFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFiles
        fields = '__all__'
        
        
class ServiceCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceComments
        fields = '__all__'
class ServiceVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceVotes
        fields = '__all__'
       

class ServiceNegotiateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceNegotiate
        fields = '__all__'

class ServiceNegotiateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceNegotiateChat
        fields = '__all__'

class ServiceQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceQuestions
        fields = '__all__'

class ServiceRequestProtoSerializer(proto_serializers.ProtoSerializer):
    name = serializers.CharField()
    id= serializers.IntegerField()
    country = serializers.CharField()
    class Meta:
        proto_class = service_pb2.GetServiceRequest
        fields = '__all__'
    def message_to_data(self, message):
        """Protobuf message -> Dict of python primitive datatypes.
        """
        return MessageToDict(message)
       

class ServiceResponseProtoSerializer(proto_serializers.ProtoSerializer):
    name = serializers.CharField()
    image = serializers.CharField()
    class Meta:
        proto_class = service_pb2.GetServiceResponse
        fields = '__all__'
    def message_to_data(self, message):
        """Protobuf message -> Dict of python primitive datatypes.
        """
        return MessageToDict(message)
       