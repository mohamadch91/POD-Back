# Create your views here.
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
import copy
from .customResponse import CustomResponse,CustomMessage
from .permissions import IsAdminUser


class NewsCategoryAdminView(APIView):
    permission_classes= [IsAdminUser]
    def get(self, request):
        page = request.GET.get("page")
        page_size=request.GET.get("page_size")
        news_categories = NewsCategory.objects.all()
        total_count = len(news_categories)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            news_categories = news_categories[page*page_size:page_size*(page+1)]
        serializer = NewsCategorySerializer(news_categories, many=True)
        final_response= {
             "total_count" : total_count,
            "data": serializer.data
        }
        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))

    def post(self, request):
        serializer = NewsCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(serializer.data, status=status.HTTP_201_CREATED,message=CustomMessage(5,"خبر"))
        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,serializer._errors))
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,data="نیاز به id است"))
        id=request.data["id"]
        news_category = get_object_or_404(NewsCategory,id=id)
        serializer = NewsCategorySerializer(news_category,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(6,"خبر"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,serializer._errors))

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,data="نیاز به id است"))
        news_category = get_object_or_404(NewsCategory,id=id)
        news_category.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(7,"خبر"))


class BannerCategoryAdminView(APIView):
    permission_classes= [IsAdminUser]

    def get(self, request):
        banner_categories = BannerCategory.objects.all()
        serializer = BannerCategorySerializer(banner_categories, many=True)
        return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(1))

    def post(self, request):
        serializer = BannerCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(serializer.data, status=status.HTTP_201_CREATED,message=CustomMessage(5,"بنر"))
        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,serializer._errors))
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,data="نیاز به id است"))
        id=request.data["id"]
        banner_category = get_object_or_404(BannerCategory,id=id)
        serializer = BannerCategorySerializer(banner_category,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(6,"بنر"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,serializer._errors))

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,data="نیاز به id است"))
        banner_category = get_object_or_404(BannerCategory,id=id)
        banner_category.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(7,"بنر"))


class NewsAdminView(APIView):
    permission_classes= [IsAdminUser]
    def get(self, request):
        id= request.GET.get('id')
        if(id != None):
            news = get_object_or_404(News,id=id)
            serializer = NewsSerializer(news)
            images = NewsImages.objects.filter(news=news)
            final_response = []
            temp = copy.copy(serializer.data)
            temp["image"] = 'content' + serializer.data["image"]
            images= []
            for x  in images:
                images.append('content/media/' + x.image)
            temp["images"] = images
            final_response.append(temp)
            return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
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
        final_response = []
        for ser in serializer.data:
            temp = copy.copy(ser)
            temp["image"] = 'content' + ser["image"]
            images= []
            for x  in images:
                images.append('content/media/' + x.image)
            final_response.append(temp)

        return CustomResponse({"data":final_response,"count" : count},status=status.HTTP_200_OK,message=CustomMessage(1))
    
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
                    return CustomResponse(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,image_serializer._errors))
            return CustomResponse(serializer.data, status=status.HTTP_201_CREATED,message=CustomMessage(5,"خبر"))
        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,serializer._errors))
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,data="نیاز به id است"))
        id=request.data["id"]
        news = get_object_or_404(News,id=id)
        serializer = NewsSerializer(news,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            if("images" in request.data):
                ids= []
                for i in request.data["images"]:
                    if(i["edited"] == True or i["edited"] == "true"):
                        if("id" in i):
                            ids.append(i["id"])
                            body ={
                                "news": id,
                                "image" : i["image"],
                                "id": i["id"]
                            }
                            image = get_object_or_404(NewsImages,id=i["id"])
                            image_ser = NewsImagesSerializer (image,data=body,partial=True)
                            if (image_ser.is_valid()):
                                image_ser.save()
                            else:
                                return CustomResponse(image_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=image_ser._errors))
                        else:
                            body ={
                                "news": id,
                                "image" : i["image"]
                            }
                            image_ser = NewsImagesSerializer (data =body)
                            if (image_ser.is_valid()):
                                image_ser.save()
                                ids.append(image_ser.data["id"])
                            else:
                                return CustomResponse(image_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=image_ser._errors))
                    else:
                        ids.append(i["id"])
                images = NewsImages.objects.filter(news=id).exclude(id__in=ids)
                images.delete()
            
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(6,"خبر"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,serializer._errors))

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,data="نیاز به id است"))
        news = get_object_or_404(News,id=id)
        news.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(7,"خبر"))
    


class BannerAdminView(APIView):
    permission_classes= [IsAdminUser]
    def get(self, request):
        id = request.GET.get('id')
        if(id == None):
            banners = Banner.objects.all()
            serializer = BannerSerializer(banners, many=True)
            return CustomResponse(serializer.data)
        banner = get_object_or_404(Banner,id=id)
        serializer = BannerSerializer(banner)
        return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(1))
    
    def post(self, request):
        serializer = BannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(serializer.data, status=status.HTTP_201_CREATED,message=CustomMessage(5,"بنر"))
        return CustomResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,serializer._errors))

    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,data="نیاز به id است"))
        id=request.data["id"]
        banner = get_object_or_404(Banner,id=id)
        serializer = BannerSerializer(banner,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(6,"بنر"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,serializer._errors))

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,data="نیاز به id است"))
        banner = get_object_or_404(Banner,id=id)
        banner.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(7,"بنر"))


class NewsCategoryView(APIView):
    def get(self, request):
        page = request.GET.get("page")
        page_size=request.GET.get("page_size")
        news_categories = NewsCategory.objects.all()
        total_count = len(news_categories)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            news_categories = news_categories[page*page_size:page_size*(page+1)]
        serializer = NewsCategorySerializer(news_categories, many=True)
        final_response= {
             "total_count" : total_count,
            "data": serializer.data
        }
        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))

class BannerCategoryView(APIView):
    def get(self, request):
        banner_categories = BannerCategory.objects.all()
        serializer = BannerCategorySerializer(banner_categories, many=True)
        return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(1))


class NewsView(APIView):
    def get(self, request):
        id = request.GET.get('id')
        if(id != None):
            news = get_object_or_404(News,id=id)
            serializer = NewsSerializer(news)
            images = NewsImages.objects.filter(news=news)
            final_response = []
            temp = copy.copy(serializer.data)
            temp["image"] = 'content' + serializer.data["image"]
            images= []
            for x  in images:
                images.append('content/media/' + x.image)
            temp["images"] = images
            final_response.append(temp)
            return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
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
        final_response = []
        for ser in serializer.data:
            temp = copy.copy(ser)
            temp["image"] = 'content' + ser["image"]
            images= []
            for x  in images:
                images.append('content/media/' + x.image)
            final_response.append(temp)

        return CustomResponse({"data":final_response,"count" : count},status=status.HTTP_200_OK,message=CustomMessage(1))
    

class BannerView(APIView):
    def get(self, request):
        banners = Banner.objects.filter(status=2)
        serializer = BannerSerializer(banners, many=True)
        return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(1))
    

