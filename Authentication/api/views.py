# Create your views here.
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import get_object_or_404
from .tests import *
from django.db import connection
from .customResponse import CustomResponse,CustomMessage


class UpdateProfileView(APIView):
    permission_classes=(IsAuthenticated,)
   
    def put (self,request):
        if('type' not in request.data or 'type' =='' ):
            return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(data="نیاز به وارد کرد تایپ هست").message)
        type=request.data["type"]
        phone=request.data["phone"]
        if(type=="real"):
            data= {}
            try:
                real_user = get_object_or_404(RealUser,user_ptr_id=request.data["pk"])
                real_user_ser=RealUserSerializer(real_user,data=request.data,partial=True)
                if(real_user_ser.is_valid()):
                    real_user_ser.save()
                    return  CustomResponse(real_user_ser.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(6,"پروفایل کاربری").message)

                else:
                    return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,legal_user_ser._errors).message)
            except:
                # assign user to a legal user and create legal user
                user = get_object_or_404(User,phone=phone)
                user_ser= UpdateUserSerializer(user,data=request.data,partial=True)
                if(user_ser.is_valid()):
                    user_ser.save()
                    data = user_ser.data
                else:
                    return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,user_ser._errors).message)
                
                # do with cursor 
                try:
                    real_data ={
                    }
                    if( "first_name" in request.data):
                        real_data["first_name"] = request.data["first_name"]
                    else:
                        real_data["first_name"] = None
                    if( "last_name" in request.data):
                        real_data["last_name"] = request.data["last_name"]
                    else:
                        real_data["last_name"] = ""
                    if( "gender" in request.data):
                        real_data["gender"] = request.data["gender"]
                    else:
                        real_data["gender"] = ""

                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO public.api_legaluser ("user_ptr_id", "last_name", "first_name", "gender")
                            VALUES (%s, %s, %s, %s)
                        """, [user.pk, real_data["last_name"], real_data["first_name"], real_data["gender"]])
                    data = data | real_data
                    return CustomResponse(data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(6,"پروفایل کاربری").message)
                except Exception as e:
                    print("Error inserting data:", e)
                    return CustomResponse(None, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,"خطا در  ورودی").message)   
        
        if(type=="legal"):
            data= {}
            try:
                legal_user = get_object_or_404(LegalUser,user_ptr_id=request.data["pk"])
                legal_user_ser=LegalUserSerializer(legal_user,data=request.data,partial=True)
                if(legal_user_ser.is_valid()):
                    legal_user_ser.save()
                    return  CustomResponse(legal_user_ser.data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(6,"پروفایل کاربری").message)

                else:
                    return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,legal_user_ser._errors).message)
            except:
                # assign user to a legal user and create legal user
                user = get_object_or_404(User,phone=phone)
                user_ser= UpdateUserSerializer(user,data=request.data,partial=True)
                if(user_ser.is_valid()):
                    user_ser.save()
                    data = user_ser.data
                else:
                    return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,user_ser._errors).message)
                
                # do with cursor 
                try:
                    legal_data ={
                    }
                    if( "company_id" in request.data):
                        legal_data["company_id"] = request.data["company_id"]
                    else:
                        legal_data["company_id"] = None
                    if( "company_name" in request.data):
                        legal_data["company_name"] = request.data["company_name"]
                    else:
                        legal_data["company_name"] = ""
                    if( "company_title" in request.data):
                        legal_data["company_title"] = request.data["company_title"]
                    else:
                        legal_data["company_title"] = ""

                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO public.api_legaluser ("user_ptr_id", "company_name", "company_id", "company_title")
                            VALUES (%s, %s, %s, %s)
                        """, [user.pk, legal_data["company_name"], legal_data["company_id"], legal_data["company_title"]])
                    data = data | legal_data
                    return CustomResponse(data,status=status.HTTP_202_ACCEPTED,message=CustomMessage(6,"پروفایل کاربری").message)
                except Exception as e:
                    print("Error inserting data:", e)
                    return CustomResponse(None, status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,"خطا در  ورودی").message)
            

        return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(3,"نیاز مند تایپ").message)



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return CustomResponse(None,status=status.HTTP_205_RESET_CONTENT,message=CustomMessage(data="خروج موفقیت آمیز بود").message)
        except Exception as e:
            return CustomResponse(None,status=status.HTTP_400_BAD_REQUEST,message=CustomMessage(data="خروج ناموفق").message)    



class OTPViewLogin(APIView):

    def get(self, request):
        serializer = RequestOTPSerializer(data=request.query_params)
        # user=get_object_or_404(User,phone=request.query_params.get('receiver'))
        if serializer.is_valid():
            data = serializer.validated_data
            otp = OTPRequest.objects.generate(data)
            return CustomResponse(data=RequestOTPResponseSerializer(otp).data,status=status.HTTP_200_OK,message=CustomMessage(1).message)

        else:
            return CustomResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST, message=CustomMessage(3,serializer._errors).message )
  
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
                return CustomResponse(res, status=status.HTTP_200_OK,message=CustomMessage(1).message)
            else:
                return CustomResponse(None,status=status.HTTP_401_UNAUTHORIZED,message=CustomMessage(data="نام کاربری و یا رمز عبور اشتباه است").message)

        else:
            return CustomResponse(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors,message=CustomMessage(3,serializer._errors).message)

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
            return CustomResponse(data=RequestOTPResponseSerializer(otp).data,status=status.HTTP_200_OK,message=CustomMessage(1).message)

        else:
            return CustomResponse(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors,message=CustomMessage(3,serializer._errors).message)
  
    def post(self, request):
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                login_data =self._handle_login(data)
                if(login_data == None):
                    return CustomResponse(None,status=status.HTTP_401_UNAUTHORIZED,message=CustomMessage(data="نام کاربری و یا رمز عبور اشتباه است").message)
                 
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
                return CustomResponse(res, status=status.HTTP_200_OK,message=CustomMessage(1).message)
            else:
                return CustomResponse(None,status=status.HTTP_401_UNAUTHORIZED,message=CustomMessage(data="نام کاربری و یا رمزعبور اشتباه است").message)

        else:
            return CustomResponse(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)

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
            return CustomResponse(data=RequestOTPResponseSerializer(otp).data,status=status.HTTP_200_OK)

        else:
            return CustomResponse(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    def post(self, request):
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                login_data =self._handle_login(data,request)
                if(login_data == False):
                    return CustomResponse({"message":"phone already exists"},status=status.HTTP_400_BAD_REQUEST)
                user_data= get_object_or_404(User,phone=data['receiver'])
                body ={
                    "amount" : 0,
                        "user" : user_data.pk
                }
                w_ser= WalletSerializer(data =body)   
                if(w_ser.is_valid()):
                    w_ser.save()
                else:
                    return CustomResponse(w_ser.errors,status = status.HTTP_400_BAD_REQUEST)
                
                ser = UserSerializer(user_data)
                # print(ser.data)
                res ={
                    "login_data" : login_data,
                    "user_data" : ser.data,
                    "wallet_data" :w_ser.data
                }
                return CustomResponse(res, status=status.HTTP_200_OK)
            
            else:
                return CustomResponse(status=status.HTTP_401_UNAUTHORIZED)

        else:
            return CustomResponse(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)

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
        return CustomResponse(None,status=status.HTTP_204_NO_CONTENT,message=CustomMessage(7,"کاربر").message)


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
        
        
        
        return CustomResponse(data=serializer.data,status=status.HTTP_200_OK,message=CustomMessage(1).message)

class LegalUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user= get_object_or_404(LegalUser,phone =user)
        serializer = LegalUserSerializer(user)
        return CustomResponse(data=serializer.data,status=status.HTTP_200_OK,message=CustomMessage(1).message)

class UserAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        page = request.GET.get('page', 0)
        page_size = request.GET.get('page_size', 10)
        users = User.objects.all()
        total_count= len(users)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            users = users[page*page_size:(page+1)*page_size]
        res= []
        for i in users:
            user= get_object_or_404(User,phone =i.phone)
            try:
                user= get_object_or_404(LegalUser,phone =i.phone)
                serializer = LegalUserSerializer(user)
            except:
                try:
                    user= get_object_or_404(RealUser,phone =i.phone)
                    serializer = RealUserSerializer(user)
                except:
                    serializer = UserSerializer(user)
            res.append(serializer.data)
        response = {
            "total_count": total_count,  
            "results": res
        }
        return CustomResponse(data=response,status=status.HTTP_200_OK,message=CustomMessage(1).message)
        


class UserStatusView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        user = get_object_or_404(User,pk=request.data["id"])
        user.status = request.data["status"]
        user.save()
        return CustomResponse(None,status=status.HTTP_202_ACCEPTED,message=CustomMessage(data="وضعیت کاربر با موفقیت تغییر کرد").message)
    

class OTPViewAdmin(APIView):
    permission_classes= [IsAdminUser]
    def get(self, request):
        page = request.GET.get('page', 0)
        page_size = request.GET.get('page_size', 10)
        otp_requests= OTPRequest.objects.all()
        otp_requests = otp_requests.order_by('-created')
        total_count= len(otp_requests)
        if(page and page_size):
            page = int(page)
            page_size = int(page_size)
            otp_requests = otp_requests[page*page_size:(page+1)*page_size]
        
        serializer = OTPRequestSerializer(otp_requests, many=True)
        response = {
            "total_count": total_count,
           
            "results": serializer.data
        }
        return CustomResponse(data=response,status=status.HTTP_200_OK,message=CustomMessage(1).message)
        



