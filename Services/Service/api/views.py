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
from .permissions import IsAuthenticatedM
import copy
from django.db.models import Case, When,Sum
from . publish import transfer
import json
class ServiceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedM]
    queryset =Service.objects.all()
    def get(self, request):
        service = Service.objects.all()
        page = request.GET.get("page")
        category = request.GET.get("category")
       
        if(category):
            service = service.filter(category = category)
        if (page):
            service = service[9*int(page):9*(int(page)+1)]
        
        serializer = ServiceSerializer(service,many=True)
        answer = []

        for i in serializer.data:
            img =''
            image  = ServiceImages.objects.filter(service=i["id"] )
            if(len(image)>0):
                image =image[0]
                img = '/service/media/'+str(image.image)
            transfer_data={
              
                "serviceCategory" : i["category"]
            }
            datas= transfer(json.dumps(transfer_data),'base_info')
            data ={
                "id":i["id"],
                "name":i["name"],
                "description":i["description"],
                "month_price":i["month_price"],
                "image":img,
                "available" : i["available_count"],
                "sold" : 2455,
                "category" : datas["category"]
            }
            answer.append(data)
       
        return Response(answer,status=status.HTTP_200_OK)
    
       
class ServiceDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Service.objects.all()
    def get(self, request):
        id =request.GET.get("id")
        if(id):
            service = get_object_or_404(Service,id = id)
            i = ServiceSerializer(service).data
            transfer_data={
                "city":service.city_id,
                "serviceBrand" : service.brand,
                "serviceCategory" : service.category,

            }
            datas= transfer(json.dumps(transfer_data),'base_info','service')
            images  = ServiceImages.objects.filter(service=i["id"] )
            image_data = ServiceImagesSerializer(images,many=True).data
            comments = ServiceComments.objects.filter(service = i["id"])
            comments_data = ServiceCommentsSerializer(comments,many=True).data
            votes = ServiceVotes.objects.filter(service=i["id"] )
            sum_votes = 0
            if(len(votes)>0):
                for k in votes:
                    sum_votes+=k.votes
                sum_votes /= len(votes)
            sum_votes =float(format(sum_votes, ".2f"))
            final_response =copy.deepcopy(i)
            final_response["city_id"] = datas["city"]
            final_response["brand"] = datas["brand"]
            final_response["category"] = datas["category"]
            final_response["images"] = image_data
            final_response["votes"] = sum_votes
            final_response["comments"] = comments_data
            
            return Response(final_response,status=status.HTTP_200_OK)
        return Response({"message" :"need id"},status=status.HTTP_400_BAD_REQUEST)
    
    

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
        user,_ = request.user
        user = json.loads(user)
        temp = copy.deepcopy(request.data)
        images = request.FILES.getlist('images')
        temp["user_id"] = user["id"]
        serializer = ServiceSerializer(data = temp)
        if(serializer.is_valid()):
            serializer.save()
            id = serializer.data["id"]
            for i in images:
                body ={
                    "service": id,
                    "image" : i
                }
                image_ser = ServiceImagesSerializer (data =body)
                if (image_ser.is_valid()):
                    image_ser.save()
                else:
                    return Response(image_ser.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class EditServiceView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Service.objects.all()
    def put(self, request):
        id = request.data["id"]
        commerce = get_object_or_404(Service,id=id)
        serializer = ServiceSerializer(commerce,data = request.data)
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
        
     
class ChangeStatusView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Service.objects.all()
    def put(self, request):
        id = request.data["id"]
        service = get_object_or_404(Service,id=id)
        service.status = request.data["status"]
        service.save()
        return Response({"message" : "status changed"},status=status.HTTP_200_OK)    
    



