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



class NewsCategoryAdminView(APIView):
    def get(self, request):
        news_categories = NewsCategory.objects.all()
        serializer = NewsCategorySerializer(news_categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        news_category = get_object_or_404(NewsCategory,id=id)
        serializer = NewsCategorySerializer(news_category,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        news_category = get_object_or_404(NewsCategory,id=id)
        news_category.delete()
        return Response("deleted",status=status.HTTP_202_ACCEPTED)


class BannerCategoryAdminView(APIView):
    def get(self, request):
        banner_categories = BannerCategory.objects.all()
        serializer = BannerCategorySerializer(banner_categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BannerCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        banner_category = get_object_or_404(BannerCategory,id=id)
        serializer = BannerCategorySerializer(banner_category,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        banner_category = get_object_or_404(BannerCategory,id=id)
        banner_category.delete()
        return Response("deleted",status=status.HTTP_202_ACCEPTED)



class NewsAdminView(APIView):
    def get(self, request):
        news = News.objects.all()
        page = request.GET.get("page")
        category = request.GET.get("category")
        page_size = request.GET.get("page_size")
        if(category != None):
            news = news.filter(category=category)
        count = len(news)
        if(page != None and page_size != None):
            page = int(page)
            page_size = int(page_size)
            start = (page)*page_size
            end = (page+1)*page_size
            news = news[start:end]
        
        serializer = NewsSerializer(news, many=True)
        images = NewsImages.objects.filter(news__in=news)
        images_serializer = NewsImagesSerializer(images,many=True)
        final_response = []
        for ser in serializer.data:
            temp = copy.copy(ser)
            temp["image"] = '/content/media/' + ser["image"]
            images= []
            for x  in images_serializer.data:
                images.append('/content/media/' + x["image"])
            final_response.append(temp)

        return Response({"data":final_response,"count" : count},status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            images = request.FILES.getlist('images')
            for image in images:
                image_serializer = NewsImagesSerializer(data={"image":image,"news":serializer.data["id"]})
                if image_serializer.is_valid():
                    image_serializer.save()
                else:
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        news = get_object_or_404(News,id=id)
        serializer = NewsSerializer(news,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        news = get_object_or_404(News,id=id)
        news.delete()
        return Response("deleted",status=status.HTTP_202_ACCEPTED)
    


class BannerAdminView(APIView):

    def get(self, request):
        id = request.GET.get('id')
        if(id == None):
            banners = Banner.objects.all()
            serializer = BannerSerializer(banners, many=True)
            return Response(serializer.data)
        banner = get_object_or_404(Banner,id=id)
        serializer = BannerSerializer(banner)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        banner = get_object_or_404(Banner,id=id)
        serializer = BannerSerializer(banner,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        banner = get_object_or_404(Banner,id=id)
        banner.delete()
        return Response("deleted",status=status.HTTP_202_ACCEPTED)


class NewsCategoryView(APIView):
    def get(self, request):
        news_categories = NewsCategory.objects.all()
        serializer = NewsCategorySerializer(news_categories, many=True)
        return Response(serializer.data)

class BannerCategoryView(APIView):
    def get(self, request):
        banner_categories = BannerCategory.objects.all()
        serializer = BannerCategorySerializer(banner_categories, many=True)
        return Response(serializer.data)


class NewsView(APIView):
    def get(self, request):
        news = News.objects.filter(status=2)
        page = request.GET.get("page")
        category = request.GET.get("category")
        page_size = request.GET.get("page_size")
        if(category != None):
            news = news.filter(category=category)
        count = len(news)
        if(page != None and page_size != None):
            page = int(page)
            page_size = int(page_size)
            start = (page)*page_size
            end = (page+1)*page_size
            news = news[start:end]
        
        serializer = NewsSerializer(news, many=True)
        images = NewsImages.objects.filter(news__in=news)
        images_serializer = NewsImagesSerializer(images,many=True)
        final_response = []
        for ser in serializer.data:
            temp = copy.copy(ser)
            temp["image"] = '/content/media/' + ser["image"]
            images= []
            for x  in images_serializer.data:
                images.append('/content/media/' + x["image"])
            final_response.append(temp)

        return Response({"data":final_response,"count" : count},status=status.HTTP_200_OK)
    

class BannerView(APIView):
    def get(self, request):
        banners = Banner.objects.filter(status=2)
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data)
    

