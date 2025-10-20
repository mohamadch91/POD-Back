from dataclasses import field, fields
from os import access
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django_grpc_framework import proto_serializers
import commerce_pb2
from google.protobuf.json_format import MessageToDict




  

class CommerceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commerce
        fields = '__all__'
        
class CommerceFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommerceFiles
        fields = '__all__'
        
class CommerceCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommerceComments
        fields = '__all__'
class CommerceVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommerceVotes
        fields = '__all__'
       
class CommerceNegotiateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommerceNegotiate
        fields = '__all__'

class CommerceQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommerceQuestions
        fields = '__all__'



class CommerceRequestProtoSerializer(proto_serializers.ProtoSerializer):
    name = serializers.CharField()
    id= serializers.IntegerField()
    country = serializers.CharField()
    class Meta:
        proto_class = commerce_pb2.GetCommerceRequest
        fields = '__all__'
    def message_to_data(self, message):
        """Protobuf message -> Dict of python primitive datatypes.
        """
        return MessageToDict(message)
       

class CommerceResponseProtoSerializer(proto_serializers.ProtoSerializer):
    name = serializers.CharField()
    image = serializers.CharField()
    class Meta:
        proto_class = commerce_pb2.GetCommerceResponse
        fields = '__all__'
    def message_to_data(self, message):
        """Protobuf message -> Dict of python primitive datatypes.
        """
        return MessageToDict(message)
       