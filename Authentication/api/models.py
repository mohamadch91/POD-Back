from urllib import request
from uuid import uuid4
from django.db import models
import random
import string
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from datetime import timedelta
from django.utils import timezone
from .sender import send_otp
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager
    """

    def create_user(self, phone, password, **extra_fields):
        # print("debug")
        if not phone:
            raise ValueError('The phone must be set')

        # password=make_password(password)       
        # return self.create_user(username, password, **extra_fields)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone,password ,**extra_fields):
        # password= '123'
        # password =make_password('123')
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    username = None
    # password = None
    phone = models.CharField( max_length = 13, unique = True)
    birth = models.DateField(blank=True,null=True)
    national_code=models.CharField(max_length=10,blank=True,null=True,unique=True)
    first_name =models.CharField(max_length=20,blank=True,null=True)
    last_name =models.CharField(max_length=20,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    picture=models.ImageField(upload_to='profile_pictures/',blank=True,null=True)
    USERNAME_FIELD='phone'
    objects = CustomUserManager()
    def __str__(self):
        return "{}".format(self.phone)
    

class LegalUser(User):
    companyName= models.CharField(max_length=50,unique=True,null=True,blank=True,db_index=True)
    companyID = models.IntegerField(unique=True,null=True,blank=True)
    companyTitle = models.CharField(max_length = 50,null=True,blank=True)
    postalCode =models.CharField(max_length = 50,null=True,blank=True)
    city = models.CharField (max_length =50,null=True,blank=True)
    Province = models.IntegerField(unique=True,null=True,blank=True)
    address =models.CharField (max_length =500,null=True,blank=True)
    
    def __str__(self):
        return "{}".format(self.phone)

class Wallet(User):
    amount = models.IntegerField(unique=True,null=True,blank=True,default = 0)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'user_waller')

class OtpRequestQuerySet(models.QuerySet):
    def is_valid(self, receiver, request, password):
        current_time = timezone.now()
        return self.filter(
            receiver=receiver,
            request_id=request,
            password=password,
            created__lt=current_time,
            created__gt=current_time-timedelta(seconds=60),

        ).exists()

class OTPManager(models.Manager):

    def get_queryset(self):
        return OtpRequestQuerySet(self.model, self._db)

    def is_valid(self, receiver, request, password):
        return self.get_queryset().is_valid(receiver, request, password)


    def generate(self, data):
        otp = self.model(receiver=data['receiver'])
        otp.save(using=self._db)
        send_otp(otp)
        return otp



def generate_otp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k=5 )
    return  ''.join(digits)


class OTPRequest(models.Model):

    request_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    receiver = models.CharField(max_length=15,blank=True,null=True)
    password = models.CharField(max_length=7, default=generate_otp)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    objects = OTPManager()

# class userIp(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     ip=models.CharField(max_length=50,blank=True,null=True)
#     device=models.CharField(max_length=50,blank=True,null=True)
#     def __str__(self):
#         return "{}".format(self.user+":"+self.ip+":"+self.device)