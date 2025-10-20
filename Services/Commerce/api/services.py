from .models import *
from django_grpc_framework.services import Service
from .serializers import *
import grpc
from google.protobuf import empty_pb2
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
import json
class CommerceService(Service):
    """
    gRPC service that allows users to be retrieved or updated.
    """

    def GetList(self, request, context):
        """
        gRPC method to get user details.
        """
        # Extract the user ID from the request
        name= request.name
        id= request.id
        country = request.country
        commerce = None
        if(id):
            commerce = Commerce.objects.filter(id=id)
        elif(name):
            commerce = Commerce.objects.filter(name__contains = name)
        elif country:
            commerce = Commerce.objects.filter(country=country)
        
        res= []
        for i in commerce:
            body ={  }
            files = CommerceFiles.objects.filter(commerce= i.id,default = True)
            files= files[0]
            body["image"] = 'commerce/media/'+str(files.file)
            body["name"]= i.name
            res.append(body)
        return CommerceResponseProtoSerializer(res).message
    



                
        
