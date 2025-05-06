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
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.shortcuts import get_object_or_404
from itertools import chain
import copy
from .tests import *
from django.db import connection


class UpdateProfileView(APIView):
    permission_classes=(IsAuthenticated,)
   
    def put (self,request):
        if('type' not in request.data or 'type' =='' ):
            return Response("neeed type",status=status.HTTP_400_BAD_REQUEST)
        type=request.data["type"]
        phone=request.data["phone"]
        if(type=="real"):
            user = RealUser.objects.get_or_create(phone=phone)
            ser=UpdateRealUserSerializer(user[0],data=request.data,partial=True)
            if(ser.is_valid()):
                ser.save()
                return Response(ser.data,status=status.HTTP_202_ACCEPTED)
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        if(type=="legal"):
            data= {}
         
            try:
                legal_user = get_object_or_404(LegalUser,user_ptr_id=request.data["pk"])
                legal_user_ser=LegalUserSerializer(legal_user,data=request.data,partial=True)
                if(legal_user_ser.is_valid()):
                    legal_user_ser.save()
                    return Response(legal_user_ser.data,status=status.HTTP_202_ACCEPTED)

                else:
                    return Response(legal_user_ser.errors,status=status.HTTP_400_BAD_REQUEST)
            except:
                # assign user to a legal user and create legal user
                user = get_object_or_404(User,phone=phone)
                user_ser= UpdateUserSerializer(user,data=request.data,partial=True)
                if(user_ser.is_valid()):
                    user_ser.save()
                    data = user_ser.data
                else:
                    return Response(user_ser.errors,status=status.HTTP_400_BAD_REQUEST)
                
                # do with cursor 
                try:
                    legal_data ={
                    }
                    if( "companyID" in request.data):
                        legal_data["companyID"] = request.data["companyID"]
                    else:
                        legal_data["companyID"] = None
                    if( "companyName" in request.data):
                        legal_data["companyName"] = request.data["companyName"]
                    else:
                        legal_data["companyName"] = ""
                    if( "companyTitle" in request.data):
                        legal_data["companyTitle"] = request.data["companyTitle"]
                    else:
                        legal_data["companyTitle"] = ""

                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO public.api_legaluser ("user_ptr_id", "companyName", "companyID", "companyTitle")
                            VALUES (%s, %s, %s, %s)
                        """, [user.pk, legal_data["companyName"], legal_data["companyID"], legal_data["companyTitle"]])
                    data = data | legal_data
                    return Response(data,status=status.HTTP_202_ACCEPTED)
                except Exception as e:
                    print("Error inserting data:", e)
                    return Response({"error": "Failed to insert data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

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



class OTPViewLogin(APIView):

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
                try:
                    user_data= get_object_or_404(LegalUser,phone =user_data.phone)
                    ser = LegalUserSerializer(user_data)
                except:
                    try:
                        user_data= get_object_or_404(RealUser,phone =user_data.phone)
                        ser = RealUserSerializer(user_data)
                    except:
                        ser = UserSerializer(user_data)
                
                wallet = get_object_or_404(Wallet,user = user_data.pk) 

                w_ser= WalletSerializer(wallet,many = False)   
                res ={
                    "login_data" : login_data,
                    "user_data" : ser.data,
                    "wallet_data" :w_ser.data 
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
        else:
            user = User.objects.create(phone=otp['receiver'] )
            created = True
            body ={
                    "amount" : 0,
                    "user" : user.pk
                }
            w_ser= WalletSerializer(data =body)   
            if(w_ser.is_valid()):
                w_ser.save()
        refresh = RefreshToken.for_user(user)

        return ObtainTokenSerializer({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'created':created
        }).data


class OTPViewLoginAdmin(APIView):

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
                if(login_data == None):
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                 
                user_data= get_object_or_404(User,phone=data['receiver'])
                ser = UserSerializer(user_data)
                try:
                    user_data= get_object_or_404(LegalUser,phone =user_data.phone)
                    ser = LegalUserSerializer(user_data)
                except:
                    try:
                        user_data= get_object_or_404(RealUser,phone =user_data.phone)
                        ser = RealUserSerializer(user_data)
                    except:
                        ser = UserSerializer(user_data)
                
                wallet = get_object_or_404(Wallet,user = user_data.pk) 

                w_ser= WalletSerializer(wallet,many = False)   
                res ={
                    "login_data" : login_data,
                    "user_data" : ser.data,
                    "wallet_data" :w_ser.data 
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
        else:
            return None
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
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                login_data =self._handle_login(data,request)
                if(login_data == False):
                    return Response({"message":"phone already exists"},status=status.HTTP_400_BAD_REQUEST)
                user_data= get_object_or_404(User,phone=data['receiver'])
                body ={
                    "amount" : 0,
                        "user" : user_data.pk
                }
                w_ser= WalletSerializer(data =body)   
                if(w_ser.is_valid()):
                    w_ser.save()
                else:
                    return Response(w_ser.errors,status = status.HTTP_400_BAD_REQUEST)
                
                ser = UserSerializer(user_data)
                # print(ser.data)
                res ={
                    "login_data" : login_data,
                    "user_data" : ser.data,
                    "wallet_data" :w_ser.data
                }
                return Response(res, status=status.HTTP_200_OK)
            
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)

    def _handle_login(self, otp,request):

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
        user= get_object_or_404(User,phone =user)
        try:
            user= get_object_or_404(LegalUser,phone =user.phone)
            serializer = LegalUserSerializer(user)
        except:
            try:
                user= get_object_or_404(RealUser,phone =user.phone)
                serializer = RealUserSerializer(user)
            except:
                serializer = UserSerializer(user)
        
        
        
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class LegalUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user= get_object_or_404(LegalUser,phone =user)
        serializer = LegalUserSerializer(user)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class UserAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


class UserStatusView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user = get_object_or_404(User,pk=request.data["id"])
        user.status = request.data["status"]
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)