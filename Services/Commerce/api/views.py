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
import math
from django.http import QueryDict
from django.db.models import Case, When
from django.db.models import Sum
#TODO return comments and votes and images in detail 
#TODO return images in list 

class CommerceListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticatedM]
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
                    sum_votes[votes['votes__sum']/len_votes] = j
                sum_votes = dict(sorted(sum_votes.items() , reverse=True))
                for k in sum_votes.values():
                    pk_in.append(k.id)
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
            image  = CommerceImages.objects.filter(commerce=i["id"] )[0]
            votes = CommerceVotes.objects.filter(commerce=i["id"] )
            sum_votes = 0
            for k in votes:
                sum_votes+=k.votes
            sum_votes /= len(votes)
            sum_votes = math.ceil(sum_votes)
            data ={
                "id":i["id"],
                "name":i["name"],
                "description":i["description"],
                "month_price":i["month_price"],
                "image":str(image.image),
                "votes" : sum_votes
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
        id =request.query_params["id"]
        commerce = get_object_or_404(Commerce,id = id)
        serializer = CommerceSerializer(commerce,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

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

    queryset =Commerce.objects.all()
    def post(self, request):
        user = request.user
        temp = copy.deepcopy(request.data)
        temp["user_id"] = user["id"]
        serializer = CommerceSerializer(temp)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class EditCommerceView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Commerce.objects.all()
    def put(self, request):
        serializer = CommerceSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_202_ACCEPTED)
        
     

class DeleteCommerceView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticatedM]

    queryset =Commerce.objects.all()
    def delete(self, request):
        commerce=  get_object_or_404(Commerce,request.data["id"])
        commerce.delete()
        
        return Response({"message" : "deleted"},status=status.HTTP_204_NO_CONTENT)
        
     
    
    



