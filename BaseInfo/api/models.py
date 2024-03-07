from django.db import models

# Create your models here.

class Province(models.Model):

    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=15)

class City(models.Model):

    id = models.AutoField(primary_key=True) 
    province = models.ForeignKey(Province,on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=15)

class CommerceCategory(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=15)

class ServiceCategory(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=15)

class CommerceBrands(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=15)

class ServiceBrands(models.Model):
    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=15)

