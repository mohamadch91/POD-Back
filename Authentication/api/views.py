import http
from re import L
from django.shortcuts import render

# Create your views here.
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.shortcuts import get_object_or_404
from itertools import chain
import copy
from drf_yasg import openapi


class UpdateProfileView(APIView):
    # permission_classes=(IsAuthenticated,)
   
    def put (self,request):
        # if('pk' not in request.data or request.data['pk'] == ''):
        #     return Response({'message': 'pk is required'}, status=status.HTTP_400_BAD_REQUEST)
        if('type' not in request.data or 'type' =='' ):
            return Response("neeed type",status=status.HTTP_400_BAD_REQUEST)
        type=request.data["type"]
        phone=request.data["phone"]
        if(type=="user"):
            user=get_object_or_404(User,phone=phone)
            ser=UpdateUserSerializer(user,data=request.data)
            if(ser.is_valid()):
                ser.save()
                return Response(ser.data,status=status.HTTP_202_ACCEPTED)
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        if(type=="legal"):
            user=get_object_or_404(LegalUser,phone=phone)
            ser=UpdateLegalUserSerializer(user,data=request.data)
            if(ser.is_valid()):
                ser.save()
                return Response(ser.data,status=status.HTTP_202_ACCEPTED)
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
       
        return Response("type not found",status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)    



class OTPViewLogin(generics.GenericAPIView):

    def get(self, request):
        
        serializer = RequestOTPSerializer(data=request.query_params)
        # user=get_object_or_404(User,phone=request.query_params.get('receiver'))
        if serializer.is_valid():
            data = serializer.validated_data
            otp = OTPRequest.objects.generate(data)
            return Response(data=RequestOTPResponseSerializer(otp).data,status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
  
    def post(self, request):
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                login_data =self._handle_login(data)
                user_data= get_object_or_404(User,phone=data['receiver'])
                ser = UserSerializer(user_data)
                print(ser.data)
                res ={
                    "login_data" : login_data,
                    "user_data" : ser.data
                }
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)

    def _handle_login(self, otp):
        
        query = User.objects.filter(phone=otp['receiver'])
        if query.exists():
            created = False
            user = query.first()

        refresh = RefreshToken.for_user(user)

        return ObtainTokenSerializer({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'created':created
        }).data
class OTPViewRegister(APIView):
    def get(self, request):
        
        serializer = RequestOTPSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            otp = OTPRequest.objects.generate(data)
            return Response(data=RequestOTPResponseSerializer(otp).data,status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    def post(self, request):
        if('type' not in request.data ):
            return Response("neeed type",status=status.HTTP_400_BAD_REQUEST)#
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                login_data =self._handle_login(data,request)
                if(login_data == False):
                    return Response({"messgae":"phone already exists"},status=status.HTTP_400_BAD_REQUEST)
                if(request.data["type"] =="legal"):
                    user_data= get_object_or_404(LegalUser,phone=data['receiver'])
                else:
                    user_data= get_object_or_404(User,phone=data['receiver'])

                ser = UserSerializer(user_data)
                # print(ser.data)
                res ={
                    "login_data" : login_data,
                    "user_data" : ser.data
                }
                return Response(res, status=status.HTTP_200_OK)
            
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)

    def _handle_login(self, otp,request):
        type=request.data["type"]
        if(type=="legal"):
            try:
                s=get_object_or_404(LegalUser,phone=otp['receiver'])
                return False
            except:    
                user = LegalUser.objects.create(phone=otp['receiver'] )
                #create wallet for students
                created = True
                refresh = RefreshToken.for_user(user)
        elif(type=="real"):
            try:
                s=get_object_or_404(Teacher,phone=otp['receiver'])
                return False
            except:    
                # user =  Teacher.objects.create(phone=otp['receiver']) #in badan ok she
                created = True
                refresh = RefreshToken.for_user(user)
    
        else:
            try:
                s=get_object_or_404(User,phone=otp['receiver'])
                return False
            except:
                    
                user = User.objects.create(phone=otp['receiver'] )
                created = True
                refresh = RefreshToken.for_user(user)

        return ObtainTokenSerializer({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'created':created
        }).data

class deleteUser(APIView):
    permission_classes=(IsAuthenticated,)

    def post(self,request):
        user=get_object_or_404(User,pk=request.data["id"])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class LegalUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user= get_object_or_404(LegalUser,phone =user)
        serializer = LegalUserSerializer(user)
        return Response(data=serializer.data,status=status.HTTP_200_OK)



# class UseripView(APIView):
#     permission_classes=(IsAuthenticated,)
#     def get(self,request):
#         id=request.query_params.get('id')
#         if(id is None):
#             ip=userIp.objects.all()
#         else:
#             ip=userIp.objects.filter(user=id)
#         serializer = userIpSerializer(ip,many=True)
#         new_data=copy.deepcopy(serializer.data)
#         for i in new_data:
#             if(i["user"] is not None):
#                 user=get_object_or_404(User,id=i["user"])
#                 i["user_phone"]=user.phone
#                 i["user_name"]=user.phone
#                 if(user.first_name is not None):
#                     i["user_name"]=user.first_name
#                 if (user.last_name is not None):
#                     i["user_name"]+=user.last_name
                
#         return Response(data=new_data,status=status.HTTP_200_OK)
#     def post(self,request):
#         x=userIp.objects.filter(user=request.data["user"],ip=request.data["ip"]).delete()
#         serializer = userIpSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)