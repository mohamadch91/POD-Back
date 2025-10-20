from django.db import models

# Create your models here.

class Province(models.Model):

    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)
class City(models.Model):
    id = models.AutoField(primary_key=True) 
    province = models.ForeignKey(Province,on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=100)

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=400)

class CommerceCategory(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)

class ServiceCategory(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)

class CommerceBrands(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)

class ServiceBrands(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)

class SaleMethod(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)

class DeliveryMethod(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)

class CommerceStatus(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)
    start = models.BooleanField()
    end = models.BooleanField()

class ServiceStatus(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)
    start = models.BooleanField(null=True,blank=True)
    end = models.BooleanField(null=True,blank=True)

class ActivityType(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)

class BusinessVariety(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)

class OrderStatus(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=100)
    start = models.BooleanField(null=True,blank=True)
    end = models.BooleanField(null=True,blank=True)