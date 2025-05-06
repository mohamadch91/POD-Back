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
from .permissions import IsAuthenticated,IsAdminUser
import copy
from django.db.models import Case, When,Sum
from .publish import get_info,get_user
import json
class ServiceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset =Service.objects.all()
    def get(self, request):
        service = Service.objects.filter(status = 1)
        page = request.GET.get("page")
        page_size=request.GET.get("page_size")
        category = request.GET.get("category")
       
        if(category):
            service = service.filter(category = category)
        if (page):
            if(page_size):
                page_size = int(page_size)
                service = service[page_size*int(page):page_size*(int(page)+1)]
            else:
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
            datas= get_info(transfer_data)
            data ={
                "id":i["id"],
                "name":i["name"],
                "description":i["description"],
                "month_price":i["month_price"],
                "image":img,
                "available" : i["available_count"],
                "sold" : 2455,
                "category" : None
            }
            if(datas):
                if(datas.baseInfo):
                    datas = datas.baseInfo
                    for j in datas:
                        if(j.key == "category"):
                            data["category"] = j.value

            answer.append(data)
       
        return Response(answer,status=status.HTTP_200_OK)
    


class ServiceListAdminView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset =Service.objects.all()
    def get(self, request):
        service = Service.objects.all()
        page = request.GET.get("page")
        page_size=request.GET.get("page_size")
        category = request.GET.get("category")
       
        if(category):
            service = service.filter(category = category)
        if (page):
            page_size = int(page_size)
            service = service[page_size*int(page):page_size*(int(page)+1)]
        
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
            datas= get_info(transfer_data)
            data ={
                "id":i["id"],
                "name":i["name"],
                "description":i["description"],
                "month_price":i["month_price"],
                "image":img,
                "available" : i["available_count"],
                "sold" : 2455,
                "category" : None,
                "status":i["status"],

            }
            if(datas):
                if(datas.baseInfo):
                    datas = datas.baseInfo
                    for j in datas:
                        if(j.key == "category"):
                            data["category"] = j.value

            answer.append(data)
       
        return Response(answer,status=status.HTTP_200_OK)
    


class ServiceActionsAdminView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        user= request.user
        temp = copy.deepcopy(request.data)
        images = request.FILES.getlist('images')
        temp["user_id"] = user.id
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
    def put(self, request):
        id = request.data["id"]
        service = get_object_or_404(Service,id=id)
        serializer = ServiceSerializer(service,data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_202_ACCEPTED)
    def delete(self, request):
        service=  get_object_or_404(Service,request.data["id"])
        service.delete()
        
        return Response({"message" : "deleted"},status=status.HTTP_204_NO_CONTENT)
    


   
class ServiceDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

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
            datas= get_info(transfer_data)
            images  = ServiceImages.objects.filter(service=i["id"] )
            image_data = ServiceImagesSerializer(images,many=True).data
          
            votes = ServiceVotes.objects.filter(service=i["id"] )
            sum_votes = 0
            if(len(votes)>0):
                for k in votes:
                    sum_votes+=k.votes
                sum_votes /= len(votes)
            sum_votes =float(format(sum_votes, ".2f"))
            final_response =copy.deepcopy(i)
            final_response["city_id"] = None
            final_response["brand"] = None
            final_response["category"] = None
            final_response["images"] = image_data
            final_response["votes"] = sum_votes
            if(datas):
                if(datas.baseInfo):
                    datas = datas.baseInfo
                    for j in datas:
                        if(j.key == "category"):
                            final_response["category"] = j.value
                        if(j.key == "brand"):
                            final_response["brand"] = j.value
                        if (j.key == "city"):
                            final_response["city"] = j.value


            
            return Response(final_response,status=status.HTTP_200_OK)
        return Response({"message" :"need id"},status=status.HTTP_400_BAD_REQUEST)
    
    

class UserServiceView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Service.objects.all()
    def get(self, request):
        user = request.user
        service = get_object_or_404(Service,user_id = user.id)
        serializer = ServiceSerializer(service,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AddServiceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Service.objects.all()
    
    
class EditServiceView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Service.objects.all()
    def put(self, request):
        id = request.data["id"]
        service = get_object_or_404(Service,id=id)
        serializer = ServiceSerializer(service,data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_202_ACCEPTED)
        
     

class DeleteServiceView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Service.objects.all()
    def delete(self, request):
        service=  get_object_or_404(Service,request.data["id"])
        service.delete()
        
        return Response({"message" : "deleted"},status=status.HTTP_204_NO_CONTENT)
        
     
class ChangeStatusView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Service.objects.all()
    def put(self, request):
        id = request.data["id"]
        service = get_object_or_404(Service,id=id)
        service.status = request.data["status"]
        service.save()
        return Response({"message" : "status changed"},status=status.HTTP_200_OK)    
    

class NegotiateServiceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset =Service.objects.all()
    def post(self, request):
        user = request.user
        temp = copy.deepcopy(request.data)
        temp["user_id"] = user.id
        serializer = ServiceNegotiateSerializer(data = temp)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class NegotiateServiceAdminView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        id = request.GET.get("id")
        if(id):
            negotiate = get_object_or_404(ServiceNegotiate,id = id)
            serializer = ServiceNegotiateSerializer(negotiate).data
            return Response(serializer,status=status.HTTP_200_OK)
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        service_id=request.GET.get("service_id")
        if service_id:
            negotiate = ServiceNegotiate.objects.filter(service=service_id)
        else:
            negotiate = ServiceNegotiate.objects.all()
        total_count = len(negotiate)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            negotiate = negotiate[page*page_size:page*page_size+page_size]
        serializer = ServiceNegotiateSerializer(negotiate,many=True).data
        final = []
        for i in serializer:
            user_id= i["user_id"]
            user = get_user(user_id)
            i["user"] = user
            final.append(i)
        final_response ={
            "total_count" : total_count,
            "data": final
        }
        return Response(final_response,status=status.HTTP_200_OK)
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        negotiate = get_object_or_404(ServiceNegotiate,id=id)
        serializer = ServiceNegotiateSerializer(negotiate,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        negotiate = get_object_or_404(ServiceNegotiate,id=id)
        negotiate.delete()
        return Response("deleted",status=status.HTTP_202_ACCEPTED)


class ServiceCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        service_id = request.GET.get("service_id")
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        if(service_id == None):
            return Response("need service id",status=status.HTTP_400_BAD_REQUEST)
            
        comment = ServiceComments.objects.filter(service=service_id)
        comment = comment.filter(reply=None)
        total_cout = len(comment)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            comment = comment[page*page_size:page*page_size+page_size]
        serializer = ServiceCommentsSerializer(comment,many=True).data
        final =[]
        for i in serializer:
            reply = ServiceComments.objects.filter(reply = i["id"])
            reply_data = ServiceCommentsSerializer(reply,many=True).data
            for j in reply_data:
                user_id= j["user_id"]
                user = get_user(user_id)
                j["user"] = user
            i["reply"] = reply_data
            user_id= i["user_id"]
            user = get_user(user_id)
            i["user"] = user
            final.append(i)

        final_response ={
            "total_count" : total_cout,
            "data": final
        }
        

        return Response(final_response,status=status.HTTP_200_OK)
    def post(self, request):
        
        serializer = ServiceCommentsSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            vote = request.data["vote"]
            if(vote):
                body = {
                    "service": request.data["service"],
                    "votes" : vote
                }
                vote_serializer = ServiceVotesSerializer(data = body)
                if(vote_serializer.is_valid()):
                    vote_serializer.save()

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        comment = get_object_or_404(ServiceComments,id=id)
        serializer = ServiceCommentsSerializer(comment,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    
class ServiceAdminCommentView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        service_id=request.GET.get("service_id")
        if service_id:
            comment = ServiceComments.objects.filter(service=service_id)
        else:
            comment = ServiceComments.objects.all()
        comment = comment.filter(reply=None)
        total_cout = len(comment)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            comment = comment[page*page_size:page*page_size+page_size]
        serializer = ServiceCommentsSerializer(comment,many=True).data
        final =[]
        for i in serializer:
        
            reply = ServiceComments.objects.filter(reply = i["id"])
            reply_data = ServiceCommentsSerializer(reply,many=True).data
            for j in reply_data:
                user_id= j["user_id"]
                user = get_user(user_id)
                j["user"] = user
            i["reply"] = reply_data
            user_id= i["user_id"]
            user = get_user(user_id)
            i["user"] = user
            final.append(i)

        final_response ={
            "total_count" : total_cout,
            "data": final
        }
        return Response(final_response,status=status.HTTP_200_OK)

    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        comment = get_object_or_404(ServiceComments,id=id)
        serializer = ServiceCommentsSerializer(comment,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        comment = get_object_or_404(ServiceComments,id=id)
        comment.delete()
        return Response("deleted",status=status.HTTP_202_ACCEPTED)


    
        

    

class ServiceQuestionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        service_id = request.GET.get("service_id")
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        if(service_id == None):
            return Response("need service id",status=status.HTTP_400_BAD_REQUEST)
            
        question = ServiceQuestions.objects.filter(service=service_id)
        total_cout = len(question)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            question = question[page*page_size:page*page_size+page_size]
        serializer = ServiceQuestionsSerializer(question,many=True).data
        final_answer = []
        for i in serializer:
            user_id= i["user_id"]
            user = get_user(user_id)
            i["user"] = user
            final_answer.append(i)
        final_response ={
            "total_count" : total_cout,
            "data": final_answer
        }
        

        return Response(final_response,status=status.HTTP_200_OK)
    def post(self, request):
        serializer = ServiceQuestionsSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        question = get_object_or_404(ServiceQuestions,id=id)
        serializer = ServiceQuestionsSerializer(question,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ServiceAdminQuestionView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        service_id=request.GET.get("service_id")
        if service_id:
            question = ServiceQuestions.objects.filter(service=service_id)
        else:
            question = ServiceQuestions.objects.all()
        total_cout = len(question)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            question = question[page*page_size:page*page_size+page_size]
        serializer = ServiceQuestionsSerializer(question,many=True).data
        final_answer = []
        for i in serializer:
            user_id= i["user_id"]
            user = get_user(user_id)
            i["user"] = user
            final_answer.append(i)
        final_response ={
            "total_count" : total_cout,
            "data": final_answer
        }
       
        return Response(final_response,status=status.HTTP_200_OK)
    def post(self, request):
        serializer = ServiceQuestionsSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        question = get_object_or_404(ServiceQuestions,id=id)
        serializer = ServiceQuestionsSerializer(question,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return Response("neeed id",status=status.HTTP_400_BAD_REQUEST)
        question = get_object_or_404(ServiceQuestions,id=id)
        question.delete()
        return Response("deleted",status=status.HTTP_202_ACCEPTED)