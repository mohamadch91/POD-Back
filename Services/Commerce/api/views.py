

from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permissions import IsAuthenticated,IsAdminUser
import copy
from django.db.models import Case, When
from django.db.models import Sum
import json
from .publish import get_user,get_info
from .customResponse import CustomResponse,CustomMessage ,convert_form_to_list

class CommerceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset =Commerce.objects.all()
    def get(self, request):
        commerce = Commerce.objects.filter(status=1)
        page = request.GET.get("page")
        page_size=request.GET.get("page_size")
        category = request.GET.get("category")
        brand = request.GET.get("brand")
        sort = request.GET.get("sort")
        total_count= len(commerce)
        if(brand):
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
            page_size = int(page_size)
            commerce = commerce[page_size*int(page):page_size*(int(page)+1)]
        
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
                "price":i["price"],
                "image":img,
                "votes" : float(format(sum_votes, ".2f"))
            }
            answer.append(data)
        final_response = {
            "total_count" : total_count,
            "list" : answer
        }
        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
    

class CommerceListAdminView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset =Commerce.objects.all()
    def get(self, request):
        commerce = Commerce.objects.all()
        page = request.GET.get("page")
        page_size=request.GET.get("page_size")
        category = request.GET.get("category")
        brand = request.GET.get("brand")
        sort = request.GET.get("sort")
        total_count= len(commerce)
        if(brand):
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
            page_size = int(page_size)
            commerce = commerce[page_size*int(page):page_size*(int(page)+1)]
        
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
                "price":i["price"],
                "image":img,
                "status":i["status"],
                "votes" : float(format(sum_votes, ".2f"))
            }
            answer.append(data)
        final_response = {
            "total_count" : total_count,
            "list" : answer
        }
        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))



class CommerceActionsAdminView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        user = request.user
        temp = copy.deepcopy(request.data)
        images = request.FILES.getlist('images')
        temp["user_id"] = user.id
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
                    return CustomResponse(image_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=image_ser._errors))
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def put(self, request):
        id = request.data["id"]
        commerce = get_object_or_404(Commerce,id=id)
        serializer = CommerceSerializer(commerce,data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            new_data=convert_form_to_list(request.data)
            if("images" in new_data):
                ids= []
                for i in new_data["images"]:
                    if(i["edited"] == True or i["edited"] == "true"):
                        if("id" in i):
                            ids.append(int(i["id"]))
                            body ={
                                "commerce": id,
                                "image" : i["image"],
                                "id": int(i["id"])
                            }
                            image = get_object_or_404(CommerceImages,id=int(i["id"]))
                            image_ser = CommerceImagesSerializer (image,data=body,partial=True)
                            if (image_ser.is_valid()):
                                image_ser.save()
                            else:
                                return CustomResponse(image_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=image_ser._errors))
                        else:
                            body ={
                                "commerce": id,
                                "image" : i["image"]
                            }
                            image_ser = CommerceImagesSerializer (data =body)
                            if (image_ser.is_valid()):
                                image_ser.save()
                                ids.append(image_ser.data["id"])
                            else:
                                return CustomResponse(image_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=image_ser._errors))
                    else:
                        ids.append(int(i["id"]))
                images = CommerceImages.objects.filter(commerce=id).exclude(id__in=ids)
                images.delete()            
            return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(type=6,data="بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def delete(self, request):
        commerce=  get_object_or_404(Commerce,id=request.data["id"])
        commerce.delete()
        return CustomResponse({"message" : "deleted"},status=status.HTTP_204_NO_CONTENT,message=CustomMessage(type=7,data="بازرگانی"))
  



class CommerceDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Commerce.objects.all()
    def get(self, request):
        id =request.GET.get("id")
        if(id):
            commerce = get_object_or_404(Commerce,id = id)
            i = CommerceSerializer(commerce).data
            transfer_data={
                "commerceBrand" : commerce.brand,
                "commerceCategory" : commerce.category
            }
            datas= get_info(transfer_data)
            
            images  = CommerceImages.objects.filter(commerce=i["id"] )
            image_data = CommerceImagesSerializer(images,many=True).data
            images_response= []
            for j in image_data:
                body ={
                    "id":j["id"],
                    "image":'commerce'+j["image"]
                }
                images_response.append(body)
           
            votes = CommerceVotes.objects.filter(commerce=i["id"] )
            sum_votes = 0
            if(len(votes)>0):
                for k in votes:
                    sum_votes+=k.votes
                sum_votes /= len(votes)
            sum_votes =float(format(sum_votes, ".2f"))
            final_response =copy.deepcopy(i)
            # final_response["city_id"] = datas["city"]
            
            final_response["images"] = images_response
            final_response["votes"] = sum_votes
            final_response["brand"] = None
            final_response["category"] = None

            if(datas):
                if(datas.baseInfo):
                    datas = datas.baseInfo
                    for j in datas:
                        if(j.key == "brand"):
                            final_response["brand"] = {
                                "id": commerce.brand,
                                "value": j.value
                            }
                        if(j.key == "category"):
                            final_response["category"] = {
                                "id": commerce.category,
                                "value": j.value
                            }
                

            return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
        return CustomResponse({"message" :"need id"},status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="بازرگانی"))

    

class UserCommerceView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Commerce.objects.all()
    def get(self, request):
        user = request.user
        commerce = Commerce.objects.filter(user_id =user.id)
        serializer = CommerceSerializer(commerce,many=True)
        return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(1))

class AddCommerceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommerceSerializer

    queryset =Commerce.objects.all()
    def post(self, request):
        user = request.user
        temp = copy.deepcopy(request.data)
        images = request.FILES.getlist('images')
        temp["user_id"] = user.id
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
                    return CustomResponse(image_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=image_ser._errors))
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))

class EditCommerceView(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CommerceSerializer
    queryset =Commerce.objects.all()
    def put(self, request):
        id = request.data["id"]
        commerce = get_object_or_404(Commerce,id=id)
        serializer = CommerceSerializer(commerce,data = request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            new_data=convert_form_to_list(request.data)
            if("images" in new_data):
                ids= []
                for i in new_data["images"]:
                    if(i["edited"] == True or i["edited"] == "true"):
                        if("id" in i):
                            ids.append(int(i["id"]))
                            body ={
                                "commerce": id,
                                "image" : i["image"],
                                "id": int(i["id"])
                            }
                            image = get_object_or_404(CommerceImages,id=int(i["id"]))
                            image_ser = CommerceImagesSerializer (image,data=body,partial=True)
                            if (image_ser.is_valid()):
                                image_ser.save()
                            else:
                                return CustomResponse(image_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=image_ser._errors))
                        else:
                            body ={
                                "commerce": id,
                                "image" : i["image"]
                            }
                            image_ser = CommerceImagesSerializer (data =body)
                            if (image_ser.is_valid()):
                                image_ser.save()
                                ids.append(image_ser.data["id"])
                            else:
                                return CustomResponse(image_ser.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=2,data=image_ser._errors))
                    else:
                        ids.append(int(i["id"]))
                images = CommerceImages.objects.filter(commerce=id).exclude(id__in=ids)
                images.delete()

            return CustomResponse(serializer.data,status=status.HTTP_200_OK,message=CustomMessage(type=6,data="بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
        
class DeleteCommerceView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset =Commerce.objects.all()
    def delete(self, request):
        commerce=  get_object_or_404(Commerce,id=request.data["id"])
        commerce.delete()
        return CustomResponse({"message" : "deleted"},status=status.HTTP_204_NO_CONTENT,message=CustomMessage(type=7,data="بازرگانی"))
        

class ChangeStatusView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset =Commerce.objects.all()
    def put(self, request):
        id = request.data["id"]
        commerce = get_object_or_404(Commerce,id=id)
        commerce.status = request.data["status"]
        commerce.save()
        return CustomResponse({"message" : "status changed"},status=status.HTTP_200_OK,message=CustomMessage(data="وضعیت بازرگانی با موفیقت تغییر کرد"))


class NegotiateCommerceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommerceNegotiateSerializer
    queryset =CommerceNegotiate.objects.all()
    def post(self, request):
        user = request.user
        temp = copy.deepcopy(request.data)
        temp["user_id"] = user.id
        serializer = CommerceNegotiateSerializer(data = temp)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="درخواست مذاکره بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    
class NegotiateCommerceAdminView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        id = request.GET.get("id")
        if(id):
            negotiate = get_object_or_404(CommerceNegotiate,id = id)
            serializer = CommerceNegotiateSerializer(negotiate).data
            return CustomResponse(serializer,status=status.HTTP_200_OK,message=CustomMessage(1))
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        commerce_id=request.GET.get("commerce_id")
        if(commerce_id):
            negotiate = CommerceNegotiate.objects.filter(commerce = commerce_id)
        else:
            negotiate = CommerceNegotiate.objects.all()
        total_count = len(negotiate)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            negotiate = negotiate[page*page_size:page*page_size+page_size]
        serializer = CommerceNegotiateSerializer(negotiate,many=True).data
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
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        negotiate = get_object_or_404(CommerceNegotiate,id=id)
        serializer = CommerceNegotiateSerializer(negotiate,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="درخواست مذاکره بازرگانی"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    
    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(data="نیازمند id "))
        negotiate = get_object_or_404(CommerceNegotiate,id=id)
        negotiate.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="درخواست مذاکره بازرگانی"))
    

class CommerceCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        commerce_id = request.GET.get("commerce_id")
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        if(commerce_id == None):
            return CustomResponse("need commerce id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
            
        comment = CommerceComments.objects.filter(commerce=commerce_id)
        # remove comments which they are reply
        comment = comment.filter(reply=None)
        total_cout = len(comment)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            comment = comment[page*page_size:page*page_size+page_size]
        serializer = CommerceCommentsSerializer(comment,many=True).data
        final =[]
        for i in serializer:
            reply = CommerceComments.objects.filter(reply = i["id"])
            reply_data = CommerceCommentsSerializer(reply,many=True).data
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
        
        serializer = CommerceCommentsSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            if("vote" in request.data):
                vote= request.data["vote"]
                if(vote):
                    body = {
                        "commerce": request.data["commerce"],
                        "votes" : vote
                    }
                    vote_serializer = CommerceVotesSerializer(data = body)
                    if(vote_serializer.is_valid()):
                        vote_serializer.save()

            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="نظر بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        id=request.data["id"]
        comment = get_object_or_404(CommerceComments,id=id)
        serializer = CommerceCommentsSerializer(comment,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="نظر بازرگانی"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        comment = get_object_or_404(CommerceComments,id=id)
        comment.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="نظر بازرگانی"))
    

    
class CommerceAdminCommentView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        commerce_id=request.GET.get("commerce_id")
        if(commerce_id):
            comment = CommerceComments.objects.filter(commerce=commerce_id)
        else:       
            comment = CommerceComments.objects.all()
        comment = comment.filter(reply=None)
        total_count = len(comment)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            comment = comment[page*page_size:page_size*(page+1)]
        serializer = CommerceCommentsSerializer(comment,many=True).data
        final =[]
        for i in serializer:
            reply = CommerceComments.objects.filter(reply = i["id"])
            reply_data = CommerceCommentsSerializer(reply,many=True).data
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
            "total_count" : total_count,
            "data": final
        }
        return CustomResponse(final_response,status=status.HTTP_200_OK,message=CustomMessage(1))
    def post(self, request):
        
        serializer = CommerceCommentsSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            if("vote" in request.data):
                vote= request.data["vote"]
                if(vote):
                    body = {
                        "commerce": request.data["commerce"],
                        "votes" : vote
                    }
                    vote_serializer = CommerceVotesSerializer(data = body)
                    if(vote_serializer.is_valid()):
                        vote_serializer.save()

            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="نظر بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    
    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST)
        id=request.data["id"]
        comment = get_object_or_404(CommerceComments,id=id)
        serializer = CommerceCommentsSerializer(comment,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="نظر بازرگانی"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        comment = get_object_or_404(CommerceComments,id=id)
        comment.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="نظر بازرگانی"))
    

       
        

    

class CommerceQuestionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        commerce_id = request.GET.get("commerce_id")
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        if(commerce_id == None):
            return CustomResponse("need commerce id",status=status.HTTP_400_BAD_REQUEST)
            
        question = CommerceQuestions.objects.filter(commerce=commerce_id)
        total_cout = len(question)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            question = question[page*page_size:page*page_size+page_size]
        serializer = CommerceQuestionsSerializer(question,many=True).data
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
        serializer = CommerceQuestionsSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="سوال بازرگانی"))
        
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        id=request.data["id"]
        question = get_object_or_404(CommerceQuestions,id=id)
        serializer = CommerceQuestionsSerializer(question,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="سوال بازرگانی"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))

class CommerceAdminQuestionView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        page= request.GET.get("page")
        page_size=request.GET.get("page_size")
        commerce_id=request.GET.get("commerce_id")
        if(commerce_id):
            question = CommerceQuestions.objects.filter(commerce=commerce_id)
        else:
            question = CommerceQuestions.objects.all()
        total_cout = len(question)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            question = question[page*page_size:page*page_size+page_size]
        serializer = CommerceQuestionsSerializer(question,many=True).data
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
        serializer = CommerceQuestionsSerializer(data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_201_CREATED,message=CustomMessage(type=5,data="سوال بازرگانی"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))
    
    def put(self, request):
        if('id' not in request.data or 'id' =='' ):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        id=request.data["id"]
        question = get_object_or_404(CommerceQuestions,id=id)
        serializer = CommerceQuestionsSerializer(question,data=request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return CustomResponse(serializer.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=6,data="سوال بازرگانی"))
        return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data=serializer._errors))

    def delete(self,request):
        id = request.GET.get('id')
        if(id == None):
            return CustomResponse("neeed id",status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(type=3,data="نیازمند id "))
        question = get_object_or_404(CommerceQuestions,id=id)
        question.delete()
        return CustomResponse("deleted",status=status.HTTP_202_ACCEPTED,message=CustomMessage(type=7,data="سوال بازرگانی"))

       
        