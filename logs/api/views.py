from django.shortcuts import render

# Create your views here.
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import copy
import math
from django.http import QueryDict
from django.db.models import Case, When
from django.db.models import Sum
import json


class PermiumRequestView(APIView):

    def post(self, request):
        serializer = PermiumRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ConsultationRequestView(APIView):


    def post(self, request):
        serializer = ConsultationRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PermiumRequestAdminView(APIView):

    def get(self, request):
        permium_requests = PermiumRequest.objects.all()
        serializer = PermiumRequestSerializer(permium_requests, many=True)
        return Response(serializer.data)
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        permium_request = get_object_or_404(PermiumRequest,id=id)
        serializer = PermiumRequestSerializer(permium_request,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        permium_request = get_object_or_404(PermiumRequest,id=id)
        permium_request.delete()
        return Response("deleted",status=status.HTTP_202_ACCEPTED)
    

class ConsultationRequestAdminView(APIView):
    
        def get(self, request):
            consultation_requests = ConsultationRequest.objects.all()
            serializer = ConsultationRequestSerializer(consultation_requests, many=True)
            return Response(serializer.data)
        
        def put (self,request):
            if('id' not in request.data or 'id' =='' ):
                return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
            id=request.data["id"]
            consultation_request = get_object_or_404(ConsultationRequest,id=id)
            serializer = ConsultationRequestSerializer(consultation_request,data=request.data,partial=True)
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        def delete(self,request):
            id = request.GET.get('id')
            if(id == None):
                return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
            consultation_request = get_object_or_404(ConsultationRequest,id=id)
            consultation_request.delete()
            return Response("deleted",status=status.HTTP_202_ACCEPTED)

class ContactUsView(APIView):

    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ContactUsAdminView(APIView):
    def get(self, request):
        contact_us = ContactUs.objects.all()
        serializer = ContactUsSerializer(contact_us, many=True)
        return Response(serializer.data)
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        contact_us = get_object_or_404(ContactUs,id=id)
        serializer = ContactUsSerializer(contact_us,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        contact_us = get_object_or_404(ContactUs,id=id)
        contact_us.delete()
        return Response("deleted",status=status.HTTP_202_ACCEPTED)