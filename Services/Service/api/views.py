import http
from re import L
from django.shortcuts import render

# Create your views here.
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permissions import auth,IsAuthenticatedM
import copy

#TODO return comments and votes and images in detail 
#TODO return images in list 

class ServiceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedM]
    queryset =Service.objects.all()
    def get(self, request):
        service = Service.objects.all()
        serializer = ServiceSerializer(service,many=True)
        #TODO  return just 3 or 4 field for card view
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ServiceDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Service.objects.all()
    def get(self, request):
        id =request.query_params["id"]
        service = get_object_or_404(Service,id = id)
        serializer = ServiceSerializer(service,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class UserServiceView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Service.objects.all()
    def get(self, request):
        user = request.user
        service = get_object_or_404(Service,user_id = user["id"])
        serializer = ServiceSerializer(service,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AddServiceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Service.objects.all()
    def post(self, request):
        user = request.user
        temp = copy.deepcopy(request.data)
        temp["user_id"] = user["id"]
        serializer = ServiceSerializer(temp)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class EditServiceView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Service.objects.all()
    def put(self, request):
        serializer = ServiceSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_202_ACCEPTED)
        
     

class DeleteServiceView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Service.objects.all()
    def delete(self, request):
        service=  get_object_or_404(Service,request.data["id"])
        service.delete()
        
        return Response({"message" : "deleted"},status=status.HTTP_204_NO_CONTENT)
        
     
    
    



