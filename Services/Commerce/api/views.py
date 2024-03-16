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
from .permissions import transfer,IsAuthenticatedM
import copy
import math
from django.http import QueryDict
from django.db.models import Case, When
from django.db.models import Sum
import json
 

class CommerceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedM]
    queryset =Commerce.objects.all()
    def get(self, request):
        commerce = Commerce.objects.all()
        page = request.GET.get("page")
        category = request.GET.get("category")
        brand = request.GET.get("brand")
        sort = request.GET.get("sort")
        total_count= len(commerce)
        if(brand):
            print(brand)
            commerce =commerce.filter(brand =brand)
            total_count = len(commerce)
        if(category):
            commerce = commerce.filter(category = category)
            total_count = len(commerce)
        if(sort):
            if(sort=="old"):
                commerce=commerce.order_by('created_at')
            if(sort=="new"):
                commerce=commerce.order_by('-created_at')
            if(sort=="pop"):
                sum_votes={}
                pk_in=[]
                for j in commerce:
                    votes= CommerceVotes.objects.filter(commerce=j).aggregate(Sum('votes'))
                    len_votes=len(CommerceVotes.objects.filter(commerce=j))
                    if(len_votes == 0):
                        sum_votes[j.id]=0    
                    else:
                        sum_votes[j.id] = votes['votes__sum']/len_votes
                sum_votes = dict(sorted(sum_votes.items(), key=lambda item: item[1],reverse=True))
                for k in sum_votes.keys():
                    pk_in.append(k)
                preferred = Case(
                       *(When(id=id, then=pos) for pos, id in enumerate(pk_in, start=1)))
                commerce = commerce.filter(id__in=pk_in).order_by(preferred)                   
                # query_dict.update(ordinary_dict)
            if(sort=="alpha"):
               commerce= commerce.order_by('name')    
                

        if (page):
            commerce = commerce[12*int(page):12*(int(page)+1)]
        
        serializer = CommerceSerializer(commerce,many=True)
        answer = []

        for i in serializer.data:
            img =''
            image  = CommerceImages.objects.filter(commerce=i["id"] )
            if(len(image)>0):
                image =image[0]
                img = 'commerce/media/'+str(image.image)
            votes = CommerceVotes.objects.filter(commerce=i["id"] )
            sum_votes = 0
            if(len(votes)>0):
                for k in votes:
                    sum_votes+=k.votes
                sum_votes /= len(votes)
          
            data ={
                "id":i["id"],
                "name":i["name"],
                "description":i["description"],
                "month_price":i["month_price"],
                "image":img,
                "votes" : float(format(sum_votes, ".2f"))
            }
            answer.append(data)
        final_response = {
            "total_count" : total_count,
            "list" : answer
        }
        return Response(final_response,status=status.HTTP_200_OK)
    
class CommerceDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Commerce.objects.all()
    def get(self, request):
        print("request")
        id =request.GET.get("id")
        if(id):
            commerce = get_object_or_404(Commerce,id = id)
            i = CommerceSerializer(commerce).data
            transfer_data={
                "city":commerce.city_id,
                "commerceBrand" : commerce.brand,
                "commerceCategory" : commerce.category
            }
            datas= transfer(json.dumps(transfer_data),'base_info')
            images  = CommerceImages.objects.filter(commerce=i["id"] )
            image_data = CommerceImagesSerializer(images,many=True).data
            img_copy = copy.deepcopy(image_data)
            for j in img_copy:
                j["image"] = 'commerce'+j["image"] 
            comments = CommerceComments.objects.filter(commerce = i["id"])
            comments_data = CommerceCommentsSerializer(comments,many=True).data
            votes = CommerceVotes.objects.filter(commerce=i["id"] )
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
            final_response["images"] = img_copy
            final_response["votes"] = sum_votes
            final_response["comments"] = comments_data

            return Response(final_response,status=status.HTTP_200_OK)
        return Response({"message" :"need id"},status=status.HTTP_400_BAD_REQUEST)
    

class UserCommerceView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Commerce.objects.all()
    def get(self, request):
        user = request.user
        commerce = get_object_or_404(Commerce,user_id = user["id"])
        serializer = CommerceSerializer(commerce,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AddCommerceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedM]
    serializer_class = CommerceSerializer

    queryset =Commerce.objects.all()
    def post(self, request):
        user,_ = request.user
        user = json.loads(user)
        temp = copy.deepcopy(request.data)
        # print(request.data["images"])
        print(request.data)
        images = request.FILES.getlist('images')
        print(images)
        temp["user_id"] = user["id"]
        serializer = CommerceSerializer(data = temp)
        if(serializer.is_valid()):
            serializer.save()
            id = serializer.data["id"]
            for i in images:
                body ={
                    "commerce": id,
                    "image" : i
                }
                image_ser = CommerceImagesSerializer (data =body)
                if (image_ser.is_valid()):
                    image_ser.save()
                else:
                    return Response(image_ser.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class EditCommerceView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticatedM]
    serializer_class = CommerceSerializer
    queryset =Commerce.objects.all()
    def put(self, request):
        id = request.data["id"]
        commerce = get_object_or_404(Commerce,id=id)
        serializer = CommerceSerializer(commerce,data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_202_ACCEPTED)
        
     

class DeleteCommerceView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Commerce.objects.all()
    def delete(self, request):
        commerce=  get_object_or_404(Commerce,id=request.data["id"])
        commerce.delete()
        return Response({"message" : "deleted"},status=status.HTTP_204_NO_CONTENT)
        
     
    
    



