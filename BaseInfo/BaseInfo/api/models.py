from django.db import models

# Create your models here.

class Province(models.Model):

    id = models.AutoField(primary_key=True) 
    value = models.CharField(max_length=15)

class City(models.Model):

    id = models.AutoField(primary_key=True) 
    province = models.ForeignKey(Province)
    value = models.CharField(max_length=15)
