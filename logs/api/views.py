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
from .customResponse import CustomResponse,CustomMessage

class PermiumRequestView(APIView):

    def post(self, request):
        serializer = PermiumRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(serializer.data, status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="درخواست پرمیوم"))
        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data="درخواست پرمیوم با خطا مواجه شد"))
    
class ConsultationRequestView(APIView):


    def post(self, request):
        serializer = ConsultationRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(serializer.data, status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="درخواست مشاوره"))
        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data="درخواست مشاوره با خطا مواجه شد"))



class PermiumRequestAdminView(APIView):

    def get(self, request):
        permium_requests = PermiumRequest.objects.all()
        serializer = PermiumRequestSerializer(permium_requests, many=True)
        return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(type=1,data="درخواست پرمیوم"))
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="درخواست پرمیوم"))
        id=request.data["id"]
        permium_request = get_object_or_404(PermiumRequest,id=id)
        serializer = PermiumRequestSerializer(permium_request,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="درخواست پرمیوم"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data="درخواست پرمیوم با خطا مواجه شد"))

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="درخواست پرمیوم"))
        permium_request = get_object_or_404(PermiumRequest,id=id)
        permium_request.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="درخواست پرمیوم"))
    

class ConsultationRequestAdminView(APIView):
    
        def get(self, request):
            consultation_requests = ConsultationRequest.objects.all()
            serializer = ConsultationRequestSerializer(consultation_requests, many=True)
            return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(type=1,data="درخواست مشاوره"))
        
        def put (self,request):
            if('id' not in request.data or 'id' =='' ):
                return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="درخواست مشاوره"))
            id=request.data["id"]
            consultation_request = get_object_or_404(ConsultationRequest,id=id)
            serializer = ConsultationRequestSerializer(consultation_request,data=request.data,partial=True)
            if(serializer.is_valid()):
                serializer.save()
                return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="درخواست مشاوره"))
            return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data="درخواست مشاوره با خطا مواجه شد"))
    
        def delete(self,request):
            id = request.GET.get('id')
            if(id == None):
                return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="درخواست مشاوره"))
            consultation_request = get_object_or_404(ConsultationRequest,id=id)
            consultation_request.delete()
            return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="درخواست مشاوره"))

class ContactUsView(APIView):

    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(serializer.data, status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="درخواست تماس با ما"))
        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data="درخواست تماس با ما با خطا مواجه شد"))
    

class ContactUsAdminView(APIView):
    def get(self, request):
        contact_us = ContactUs.objects.all()
        serializer = ContactUsSerializer(contact_us, many=True)
        return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(type=1,data="درخواست تماس با ما"))
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="درخواست تماس با ما"))
        id=request.data["id"]
        contact_us = get_object_or_404(ContactUs,id=id)
        serializer = ContactUsSerializer(contact_us,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="درخواست تماس با ما"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data="درخواست تماس با ما با خطا مواجه شد"))

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="درخواست تماس با ما"))
        contact_us = get_object_or_404(ContactUs,id=id)
        contact_us.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="درخواست تماس با ما"))