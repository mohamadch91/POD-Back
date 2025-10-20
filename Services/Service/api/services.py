from ...Search.api.models import *
from django_grpc_framework.services import Service
from ...Search.api.serializers import *
import grpc
from google.protobuf import empty_pb2
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
import json
class ServiceService(Service):
    """
    gRPC service that allows users to be retrieved or updated.
    """

    def GetList(self, request, context):
        """
        gRPC method to get user details.
        """
        # Extract the user ID from the request
        base_info= request.baseInfo
        final_response =[]
       
        return BaseInfoRequestProtoSerializer(res).message
    



                
        
