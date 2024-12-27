from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Commerce(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length = 200,null =True,blank =True)
    year = models.IntegerField(null =True,blank =True)
    weight = models.IntegerField(null =True,blank =True)
    lentgh = models.FloatField(null=True,blank=True)
    width = models.FloatField(null=True,blank=True)
    height = models.FloatField(null=True,blank=True)
    description = models.TextField(max_length =1000,null =True,blank =True)
    user_id =models.IntegerField(null =True,blank =True)
    price = models.IntegerField(null =True,blank =True)
    unit = models.CharField(null=True,blank=True,max_length = 200)
    code = models.CharField(max_length = 200,null =True,blank =True)
    logistic_price =models.IntegerField(null =True,blank =True)
    discount = models.IntegerField(null =True,blank =True)
    category = models.IntegerField(null =True,blank =True)
    brand = models.IntegerField(null =True,blank =True)
    available_count =models.IntegerField(null =True,blank =True)
    free_transport = models.BooleanField(null =True,blank =True)
    status = models.IntegerField(default=0,null=True,blank=True)
    fair_price = models.BooleanField(default=True,null =True,blank =True)
    valid_seller = models.BooleanField(default=True,null =True,blank =True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class CommerceImages(models.Model):
    id = models.AutoField(primary_key=True) 
    image = models.ImageField(upload_to='images')
    commerce = models.ForeignKey(Commerce,db_index= True , on_delete= models.CASCADE)


class CommerceComments(models.Model):
    id = models.AutoField(primary_key=True) 
    comment = models.CharField(max_length = 200)
    commerce = models.ForeignKey(Commerce,db_index= True , on_delete= models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class CommerceVotes(models.Model):
    id = models.AutoField(primary_key=True) 
    votes = models.IntegerField()
    commerce = models.ForeignKey(Commerce,db_index= True , on_delete= models.CASCADE)

