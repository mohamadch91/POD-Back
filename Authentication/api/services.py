from .models import *
from django_grpc_framework.services import Service
from .serializers import *
import grpc
from google.protobuf import empty_pb2
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
class UserService(Service):
    """
    gRPC service that allows users to be retrieved or updated.
    """
    def Authentication(self, request, context):
        """
        gRPC method to authenticate a user.
        """
        # Extract the user ID from the request
        JWT_authenticator = JWTAuthentication()
        jwt= request.jwt

            # authenitcate() verifies and decode the token
            # if token is invalid, it raises an exception and returns 401

        try:
            v_token = JWT_authenticator.get_validated_token(jwt)
            response = JWT_authenticator.get_user(v_token)
            if response is not None:
                # unpacking
                ser = UserProtoSerializer(response)
                return ser.message
        except:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Invalid token')
            return empty_pb2.Empty()
    def GetUser(self, request, context):
        """
        gRPC method to get user details.
        """
        # Extract the user ID from the request
        user_id = request.id
        try:
            user= get_object_or_404(User,pk =user_id)
            if(isinstance(user, LegalUser)):
                serializer = LegallUserProtoSerializer(user)
            elif(isinstance(user, RealUser)):
                    serializer =RealUserProtoSerializer(user)
            else:
                serializer = UserProtoSerializer(user)
            return serializer.message
        except Exception as e:
            print(e)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            context.abort()

    

                
        
