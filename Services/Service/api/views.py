
# Create your views here.
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permissions import IsAuthenticated,IsAdminUser
import copy
from .publish import get_info,get_user
from .customResponse import CustomResponse,CustomMessage,convert_form_to_list
class ServiceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset =Service.objects.all()
    def get(self, request):
        service = Service.objects.filter(status = 1)
        page = request.GET.get("page")
        page_size=request.GET.get("page_size")
        category = request.GET.get("category")
       
        if(category):
            service = service.filter(category = category).order_by("-updated_at")
        total_count = len(service)
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
            file  = ServiceFiles.objects.filter(service=i["id"],default=True)
            if(len(file)>0):
                file =file[0]
                img = '/service/media/'+str(file.file)
            transfer_data={
              
                "serviceCategory" : i["category"]
            }
            datas= get_info(transfer_data)
            data ={
                "id":i["id"],
                "name":i["name"],
                "description":i["description"],
                "month_price":i["month_price"],
                "file":img,
                "available" : i["available_count"],
                "category" : None
            }
            if(datas):
                if(datas.baseInfo):
                    datas = datas.baseInfo
                    for j in datas:
                        if(j.key == "category"):
                            data["category"] = j.value

            answer.append(data)
        final_answer={
            "total_count" : total_count,
            "data": answer
        }
       
        return CustomResponse(final_answer,status=status.HTTP_200_OK,message=CustomMessage(1))
    


class ServiceListAdminView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset =Service.objects.all()
    def get(self, request):
        service = Service.objects.all()
        page = request.GET.get("page")
        page_size=request.GET.get("page_size")
        category = request.GET.get("category")
       
        if(category):
            service = service.filter(category = category).order_by("-updated_at")
        total_count = len(service)
        if (page):
            page_size = int(page_size)
            service = service[page_size*int(page):page_size*(int(page)+1)]
        
        serializer = ServiceSerializer(service,many=True)
        answer = []

        for i in serializer.data:
            img =''
            file  = ServiceFiles.objects.filter(service=i["id"],default=True )
            if(len(file)>0):
                file =file[0]
                img = '/service/media/'+str(file.file)
            transfer_data={
              
                "serviceCategory" : i["category"]
            }
            datas= get_info(transfer_data)
            data ={
                "id":i["id"],
                "name":i["name"],
                "description":i["description"],
                "month_price":i["month_price"],
                "file":img,
                "available" : i["available_count"],
                "category" : None,
                "status":i["status"],
                "is_active":i["is_active"],

            }
            if(datas):
                if(datas.baseInfo):
                    datas = datas.baseInfo
                    for j in datas:
                        if(j.key == "category"):
                            data["category"] = j.value

            answer.append(data)
        
        final_answer={
            "total_count" : total_count,
            "data": answer
        }
       
        return CustomResponse(final_answer,status=status.HTTP_200_OK,message=CustomMessage(1))
    


class ServiceActionsAdminView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        user= request.user
        temp = copy.deepcopy(request.data)
        files = request.FILES.getlist('files')
        temp["user_id"] = user.id
        serializer = ServiceSerializer(data = temp)
        if(serializer.is_valid()):
            serializer.save()
            id = serializer.data["id"]
            for i in files:
                body ={
                    "service": id,
                    "file" : i,
                    "default":i["default"],
                }
                file_ser = ServiceFilesSerializer (data =body)
                if (file_ser.is_valid()):
                    file_ser.save()
                else:
                    return CustomResponse(file_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=file_ser._errors))
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="سرویس"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def put(self, request):
        id = request.data["id"]
        service = get_object_or_404(Service,id=id)
        serializer = ServiceSerializer(service,data = request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            new_data= convert_form_to_list(request.data)
            if("files" in new_data):
                ids= []
                for i in new_data["files"]:
                    if(i["edited"] == True or i["edited"] == "true"):
                        if("id" in i):
                            ids.append(int(i["id"]))
                            body ={
                                "service": id,
                                "file" : i["file"],
                                "id": int(i["id"]),
                                "default":i["default"],
                            }
                            file = get_object_or_404(ServiceFiles,id=int(i["id"]))
                            file_ser = ServiceFilesSerializer (file,data=body,partial=True)
                            if (file_ser.is_valid()):
                                file_ser.save()
                            else:
                                return CustomResponse(file_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=file_ser._errors))
                        else:
                            body ={
                                "service": id,
                                "file" : i["file"],
                                "default":i["default"],
                            }
                            file_ser = ServiceFilesSerializer (data =body)
                            if (file_ser.is_valid()):
                                file_ser.save()
                                ids.append(file_ser.data["id"])
                            else:
                                return CustomResponse(file_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=file_ser._errors))
                    else:
                        ids.append(int(i["id"]))
                files = ServiceFiles.objects.filter(service=id).exclude(id__in=ids)
                files.delete()
            
            return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(type=6,data="سرویس"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def delete(self, request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        service=  get_object_or_404(Service,id=id)
        service.delete()
        
        return CustomResponse({"message" : "deleted"},status=status.HTTP_204_NO_CONTENT,message=CustomMessage(type=7,data="سرویس"))
    


   
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
                "country": service.country,

            }
            datas= get_info(transfer_data)
            files  = ServiceFiles.objects.filter(service=i["id"] )
            file_data = ServiceFilesSerializer(files,many=True).data
            files_response=[]
            for j in file_data:
                body ={
                    "id":j["id"],
                    "file":'service'+j["file"],
                    "default":j["default"]


                }
                files_response.append(body)


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
            final_response["files"] = files_response
            final_response["votes"] = sum_votes
            if(datas):
                if(datas.baseInfo):
                    datas = datas.baseInfo
                    for j in datas:
                        if(j.key == "category"):
                            final_response["category"] = {
                                "id": service.brand,
                                "value": j.value
                            }
                        if(j.key == "brand"):
                            final_response["brand"] = {
                                "id": service.brand,
                                "value":j.value
                            }
                        if (j.key == "city"):
                            final_response["city"] = {
                                "id": service.city_id,
                                "value": j.value
                            }
                        if (j.key == "country"):
                            final_response["country"] = {
                                "id": service.country,
                                "value": j.value
                            }


            
            return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
        return CustomResponse({"message" :"need id"},status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="سرویس"))
    
    

class UserServiceView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Service.objects.all()
    def get(self, request):
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        is_active= request.GET.get("is_active")
        status_param= request.GET.get("status")
        category = request.GET.get("category")
        user = request.user
        service = Service.objects.filter(user_id =user.id).order_by("-updated_at")
        if(is_active):
            if(is_active == True or is_active=='true'):
                service= service.filter(is_active=True)
            else:
                service= service.filter(is_active=False)
        if(status_param):
            service= service.filter(status=int(status_param))
       
        if(category):
            service = service.filter(category = category)
        total_count = len(service)
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
            file  = ServiceFiles.objects.filter(service=i["id"],default=True )
            if(len(file)>0):
                file =file[0]
                img = '/service/media/'+str(file.file)
            transfer_data={
              
                "serviceCategory" : i["category"]
            }
            datas= get_info(transfer_data)
            data ={
                "id":i["id"],
                "name":i["name"],
                "description":i["description"],
                "month_price":i["month_price"],
                "file":img,
                "available" : i["available_count"],
                "category" : None
            }
            if(datas):
                if(datas.baseInfo):
                    datas = datas.baseInfo
                    for j in datas:
                        if(j.key == "category"):
                            data["category"] = j.value

            answer.append(data)
        final_answer={
            "total_count" : total_count,
            "data": answer
        }
        return CustomResponse(final_answer,status=status.HTTP_200_OK,message=CustomMessage(1))

class AddServiceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset =Service.objects.all()
    def post(self, request):
        user= request.user
        temp = copy.deepcopy(request.data)
        temp["user_id"] = user.id
        serializer = ServiceSerializer(data = temp)
        new_data=convert_form_to_list(request.data)
        if(serializer.is_valid()):
            serializer.save()
            id = serializer.data["id"]
            if 'files' in new_data:
                files = new_data['files']
                for i in files:
                    body ={
                        "service": id,
                        "file" : i["file"],
                        "default":i["default"],
                    }
                    file_ser = ServiceFilesSerializer (data =body)
                    if (file_ser.is_valid()):
                        file_ser.save()
                    else:
                        return CustomResponse(file_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=file_ser._errors))
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="سرویس"))

    
class EditServiceView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Service.objects.all()
    def put(self, request):
        id = request.data["id"]
        service = get_object_or_404(Service,id=id)
        serializer = ServiceSerializer(service,data = request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            new_data= convert_form_to_list(request.data)
            if("files" in new_data):
                ids= []
                for i in new_data["files"]:
                    if(i["edited"] == True or i["edited"] == "true"):
                        if("id" in i):
                            ids.append(int(i["id"]))
                            body ={
                                "service": id,
                                "file" : i["file"],
                                "id": int(i["id"]),
                                "default":i["default"],
                            }
                            file = get_object_or_404(ServiceFiles,id=int(i["id"]))
                            file_ser = ServiceFilesSerializer (file,data=body,partial=True)
                            if (file_ser.is_valid()):
                                file_ser.save()
                            else:
                                return CustomResponse(file_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=file_ser._errors))
                        else:
                            body ={
                                "service": id,
                                "file" : i["file"],
                                "default":i["default"],

                            }
                            file_ser = ServiceFilesSerializer (data =body)
                            if (file_ser.is_valid()):
                                file_ser.save()
                                ids.append(file_ser.data["id"])
                            else:
                                return CustomResponse(file_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=file_ser._errors))
                    else:
                        ids.append(int(i["id"]))
                files = ServiceFiles.objects.filter(service=id).exclude(id__in=ids)
                files.delete()
            
            return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(type=6,data="سرویس"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
        
     

class DeleteServiceView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Service.objects.all()
    def delete(self, request):
        service=  get_object_or_404(Service,request.data["id"])
        service.delete()
        
        return CustomResponse({"message" : "deleted"},status=status.HTTP_204_NO_CONTENT,message=CustomMessage(type=7,data="سرویس"))
        
     
class ChangeStatusView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Service.objects.all()
    def put(self, request):
        id = request.data["id"]
        service = get_object_or_404(Service,id=id)
        service.status = request.data["status"]
        service.save()
        return CustomResponse({"message" : "status changed"},status=status.HTTP_200_OK,message=CustomMessage(data="تغییر وضعیت موفیقت آمیز بود"))    
    

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
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="درخواست مذاکره"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    
class NegotiateChatServiceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user_id = request.GET.get("user_id")
        service_id = request.GET.get("service_id")
        negotiate_id= request.GET.get("negotiate_id")
        if (user_id and not service_id and not negotiate_id):
            if int(user_id) != request.user.id:
                return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="کاربر دسترسی به دیدن این مذاکره ها ندارد"))
            negotiates = ServiceNegotiate.objects.filter(user_id=user_id)
            res=[]
            for i in negotiates:
                ser_data=ServiceNegotiateSerializer(i).data
                chats = ServiceNegotiateChat.objects.filter(negotiate=i.id).order_by("-updated_at")
                chat_data = ServiceNegotiateChatSerializer(chats,many=True).data
                ser_data["chats"] = chat_data
                ser_data["service_name"] = i.service.name
                res.append(ser_data)
            return CustomResponse(res,status=status.HTTP_200_OK,message=CustomMessage(1))
            
        elif service_id and not user_id and not negotiate_id:
            service = get_object_or_404(Service,id=service_id)
            if  service.user_id!= request.user.id:
                return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="کاربر دسترسی به دیدن این مذاکره ها ندارد"))
            negotiates = ServiceNegotiate.objects.filter(service= service.id).order_by("-updated_at")
            ser_data = ServiceNegotiateSerializer(negotiates,many=True).data
            return CustomResponse(ser_data,status=status.HTTP_200_OK,message=CustomMessage(1))
        
        elif negotiate_id and not user_id and not service_id:
            negotiate = get_object_or_404(ServiceNegotiate,id = negotiate_id)
            if  negotiate.user_id!= request.user.id or negotiate.service.user_id != request.user.id:
                return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="کاربر دسترسی به دیدن این مذاکره ها ندارد"))
            ser_data = ServiceNegotiateSerializer(negotiate).data
            chats=ServiceNegotiateChat.objects.filter(negotiate= negotiate.id).order_by("-updated_at")
            chat_data = ServiceNegotiateChatSerializer(chats,many=True).data
            ser_data["chats"]= chat_data
            return CustomResponse(ser_data,status=status.HTTP_200_OK,message=CustomMessage(1))

        else:
            return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="just one param is required"))

    def post(self, request):
        requested_user = request.user
        if "negotiate" not in request.data:
            return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="negotiate is required"))
        negotiate = get_object_or_404(ServiceNegotiate,id=request.data["negotiate"])
        if requested_user.id != negotiate.user_id or requested_user.id != negotiate.service.user_id:
            return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="کاربر دسترسی به این مذاکره ندارد."))
        serializer = ServiceNegotiateChatSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="درخواست مذاکره بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def put(self, request):
        requested_user = request.user
        negotiate_chat = get_object_or_404(ServiceNegotiateChat,id=request.data["id"])
        if requested_user.id != negotiate_chat.user_id :
            return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="کاربر دسترسی به این مذاکره ندارد."))
        serializer = ServiceNegotiateChatSerializer(negotiate_chat,data = request.data,partial =True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="درخواست مذاکره بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def delete(self, request):
        requested_user = request.user
        id = request.GET.get('id')
        negotiate_chat = get_object_or_404(ServiceNegotiateChat,id=id)
        if requested_user.id != negotiate_chat.user_id :
            return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="کاربر دسترسی به این مذاکره ندارد."))
        negotiate_chat.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="درخواست مذاکره بازرگانی"))



class NegotiateChatAdminServiceView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        user_id = request.GET.get("user_id")
        service_id = request.GET.get("service_id")
        negotiate_id= request.GET.get("negotiate_id")
        if (user_id and not service_id and not negotiate_id):
            negotiates = ServiceNegotiate.objects.filter(user_id=user_id).order_by("-updated_at")
            res=[]
            for i in negotiates:
                ser_data=ServiceNegotiateSerializer(i).data
                chats = ServiceNegotiateChat.objects.filter(negotiate=i.id).order_by("-updated_at")
                chat_data = ServiceNegotiateChatSerializer(chats,many=True).data
                ser_data["chats"] = chat_data
                ser_data["service_name"] = i.service.name
                res.append(ser_data)
            return CustomResponse(res,status=status.HTTP_200_OK,message=CustomMessage(1))
            
        elif service_id and not user_id and not service_id:
            service = get_object_or_404(Service,id=service_id)
            negotiates = ServiceNegotiate.objects.filter(service= service.id).order_by("-updated_at")
            ser_data = ServiceNegotiateSerializer(negotiates,many=True).data
            return CustomResponse(ser_data,status=status.HTTP_200_OK,message=CustomMessage(1))
        
        elif negotiate_id and not user_id and not service_id:
            negotiate = get_object_or_404(ServiceNegotiate,id = negotiate_id)
            ser_data = ServiceNegotiateSerializer(negotiate).data
            chats=ServiceNegotiateChat.objects.filter(negotiate= negotiate.id).order_by("-updated_at")
            chat_data = ServiceNegotiateChatSerializer(chats,many=True).data
            ser_data["chats"]= chat_data
            return CustomResponse(ser_data,status=status.HTTP_200_OK,message=CustomMessage(1))

        else:
            return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="just one param is required"))

    def post(self, request):
        serializer = ServiceNegotiateChatSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="درخواست مذاکره بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def put(self, request):
        negotiate_chat = get_object_or_404(ServiceNegotiateChat,id=request.data["id"])
        serializer = ServiceNegotiateChatSerializer(negotiate_chat,data = request.data,partial =True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="درخواست مذاکره بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def delete(self, request):
        id = request.GET.get('id')
        negotiate_chat = get_object_or_404(ServiceNegotiateChat,id=id)
        negotiate_chat.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="درخواست مذاکره بازرگانی"))


        


class NegotiateServiceAdminView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        id = request.GET.get("id")
        if(id):
            negotiate = get_object_or_404(ServiceNegotiate,id = id)
            serializer = ServiceNegotiateSerializer(negotiate).data
            return CustomResponse(serializer,status=status.HTTP_200_OK,message=CustomMessage(1))
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        service_id=request.GET.get("service_id")
        if service_id:
            negotiate = ServiceNegotiate.objects.filter(service=service_id).order_by("-updated_at")
        else:
            negotiate = ServiceNegotiate.objects.all().order_by("-updated_at")
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
        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
    
    def put (self,request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        id=request.data["id"]
        negotiate = get_object_or_404(ServiceNegotiate,id=id)
        serializer = ServiceNegotiateSerializer(negotiate,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="درخواست مذاکره"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        negotiate = get_object_or_404(ServiceNegotiate,id=id)
        negotiate.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="درخواست مذاکره"))


class ServiceCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        service_id = request.GET.get("service_id")
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        if(service_id == None):
            return CustomResponse("need service id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
            
        comment = ServiceComments.objects.filter(service=service_id).order_by("-updated_at")
        comment = comment.filter(reply=None).order_by("-updated_at")
        total_cout = len(comment)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            comment = comment[page*page_size:page*page_size+page_size]
        serializer = ServiceCommentsSerializer(comment,many=True).data
        final =[]
        for i in serializer:
            reply = ServiceComments.objects.filter(reply = i["id"]).order_by("-updated_at")
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
        

        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
    def post(self, request):
        
        serializer = ServiceCommentsSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            if("vote" in request.data):
                vote = request.data["vote"]
                if(vote):
                    body = {
                        "service": request.data["service"],
                        "votes" : vote
                    }
                    vote_serializer = ServiceVotesSerializer(data = body)
                    if(vote_serializer.is_valid()):
                        vote_serializer.save()

            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="نظر"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        id=request.data["id"]
        comment = get_object_or_404(ServiceComments,id=id)
        serializer = ServiceCommentsSerializer(comment,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="نظر"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    

    
class ServiceAdminCommentView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        service_id=request.GET.get("service_id")
        if service_id:
            comment = ServiceComments.objects.filter(service=service_id).order_by("-updated_at")
        else:
            comment = ServiceComments.objects.all().order_by("-updated_at")
        comment = comment.filter(reply=None)
        total_cout = len(comment)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            comment = comment[page*page_size:page*page_size+page_size]
        serializer = ServiceCommentsSerializer(comment,many=True).data
        final =[]
        for i in serializer:
        
            reply = ServiceComments.objects.filter(reply = i["id"]).order_by("-updated_at")
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
        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
    def post(self, request):
        
        serializer = ServiceCommentsSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            if("vote" in request.data):
                vote = request.data["vote"]
                if(vote):
                    body = {
                        "service": request.data["service"],
                        "votes" : vote
                    }
                    vote_serializer = ServiceVotesSerializer(data = body)
                    if(vote_serializer.is_valid()):
                        vote_serializer.save()

            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="نظر"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        id=request.data["id"]
        comment = get_object_or_404(ServiceComments,id=id)
        serializer = ServiceCommentsSerializer(comment,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="نظر"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    
    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        comment = get_object_or_404(ServiceComments,id=id)
        comment.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="نظر"))


    
   
class ServiceQuestionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        service_id = request.GET.get("service_id")
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        if(service_id == None):
            return CustomResponse("need service id",status=status.HTTP_400_BAD_REQUEST)
        question = ServiceQuestions.objects.filter(service=service_id).order_by("-updated_at")
        empty_answer = question.filter(answer=None,status=1).order_by("-updated_at")
        answered= question.filter(status=4).order_by("-updated_at")
        final_questions = empty_answer| answered
        total_cout = len(question)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            final_questions = final_questions[page*page_size:page*page_size+page_size]
        serializer = ServiceQuestionsSerializer(final_questions,many=True).data
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
        

        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
    def post(self, request):
        serializer = ServiceQuestionsSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="سوال بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        id=request.data["id"]
        question = get_object_or_404(ServiceQuestions,id=id)
        if(question.status >=3):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=" سوال قابل ویرایش نیست "))

        if(request.user.id != question.user_id):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=" دسترسی شما کافی نیست "))

        serializer = ServiceQuestionsSerializer(question,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="سوال بازرگانی"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def delete(self,request):
        id = request.GET.get('id')
        question = get_object_or_404(ServiceQuestions,id=id)
        if(request.user.id != question.user_id):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=" دسترسی شما کافی نیست "))
        question.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="سوال بازرگانی"))



class ServiceAdminQuestionView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        service_id=request.GET.get("service_id")
        service_status= request.GET.get("status")
        if(service_id):
            question = ServiceQuestions.objects.filter(service=service_id).order_by("-updated_at")
        else:
            question = ServiceQuestions.objects.all().order_by("-updated_at")
        if service_status:
            question = question.filter(status=service_status)
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
        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
    
    def post(self, request):
        serializer = ServiceQuestionsSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="سوال بازرگانی"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    
    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        id=request.data["id"]
        question = get_object_or_404(ServiceQuestions,id=id)
        serializer = ServiceQuestionsSerializer(question,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="سوال بازرگانی"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        question = get_object_or_404(ServiceQuestions,id=id)
        question.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="سوال بازرگانی"))


class ServiceQuestionAnswerView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        service_id=request.GET.get("service_id")
        service_status= request.GET.get("status")
        if not service_id:
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        service = get_object_or_404(Service,id= service_id)
        if(service.user_id != request.user.id):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=" دسترسی شما کافی نیست "))
        question = ServiceQuestions.objects.filter(service=service_id,status__in=[1,3,5]).order_by("-updated_at")
        if service_status:
            question = question.filter(status=service_status).order_by("-updated_at")
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
        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
    
    def post(self,request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        id=request.data["id"]
        question = get_object_or_404(ServiceQuestions,id=id)
        if(request.user.id != question.service.user_id):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=" دسترسی شما کافی نیست "))
        if(question.status !=1):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=" دسترسی شما کافی نیست "))

        edited_data ={
            "answer": request.data["answer"],
            "id":id,
            "status": 3

        }
        serializer = ServiceQuestionsSerializer(question,data=edited_data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="سوال بازرگانی"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def put(self,request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        id=request.data["id"]
        question = get_object_or_404(ServiceQuestions,id=id)
        if(request.user.id != question.service.user_id):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=" دسترسی شما کافی نیست "))
        if(question.status <3):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=" دسترسی شما کافی نیست "))

        edited_data ={
            "answer": request.data["answer"],
            "id":id,

        }
        if question.status ==5 or question.status ==4 :
            edited_data["status"] = 3
        serializer = ServiceQuestionsSerializer(question,data=edited_data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="سوال بازرگانی"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))



class ServiceAdminQuestionConfirmView(APIView):
    permission_classes = [IsAdminUser]
    def post(self,request):
        data = request.data
        for i in data:
            question = get_object_or_404(ServiceQuestions,id=i["id"])
            question.status = i["status"]
            if "reject_reason" in i:
                question.reject_reason = i["reject_reason"]
            question.save()
        return CustomResponse([],status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="سوال بازرگانی"))
        
        
        
