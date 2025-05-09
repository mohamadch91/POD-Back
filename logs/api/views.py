# Create your views here.
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
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
        page = request.GET.get("page")
        page_size=request.GET.get("page_size")
        permium_requests = PermiumRequest.objects.all()
        total_count = len(permium_requests)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            permium_requests = permium_requests[page*page_size:page_size*(page+1)]
        serializer = PermiumRequestSerializer(permium_requests, many=True)
        final_response= {
             "total_count" : total_count,
            "data": serializer.data
        }
        
        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(type=1))
    
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
            page = request.GET.get("page")
            page_size=request.GET.get("page_size")
            consultation_requests = ConsultationRequest.objects.all()
            total_count = len(consultation_requests)
            if(page and page_size):
                page = int(page)
                page_size = int(page_size)
                consultation_requests = consultation_requests[page*page_size:page_size*(page+1)]
            serializer = ConsultationRequestSerializer(consultation_requests, many=True)
            final_response= {
             "total_count" : total_count,
            "data": serializer.data
                }
            return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(type=1))
        
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
        page = request.GET.get("page")
        page_size=request.GET.get("page_size")
        contact_us = ContactUs.objects.all()
        total_count = len(contact_us)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            contact_us = contact_us[page*page_size:page_size*(page+1)]
        serializer = ContactUsSerializer(contact_us, many=True)
        final_response= {
             "total_count" : total_count,
            "data": serializer.data
        }
        return CustomResponse(data=final_response,status=status.HTTP_200_OK,message=CustomMessage(type=1))
    
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