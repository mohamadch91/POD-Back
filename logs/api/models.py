from django.db import models

# Create your models here.

class ConsultationRequest (models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PermiumRequest (models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class ContactUs (models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=1000)
    method = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)