from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Service(models.Model):

    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length = 200)
    year = models.IntegerField(null =True,blank =True)
    weight = models.FloatField(null =True,blank =True)
    dimensions= models.FloatField(null=True,blank=True)
    city_id = models.IntegerField(null =True,blank =True)
    description = models.TextField(max_length =500)
    user_id =models.IntegerField(null =True,blank =True)
    day_price = models.IntegerField(null =True,blank =True)
    month_price = models.IntegerField(null =True,blank =True)
    unit = models.CharField(null=True,blank=True,max_length = 200)
    code = models.CharField(max_length = 200)
    logistic_price =models.IntegerField(null =True,blank =True)
    free_transport = models.BooleanField(null =True,blank =True)
    discount = models.IntegerField(null =True,blank =True)
    category = models.IntegerField(null =True,blank =True)
    brand = models.IntegerField(null =True,blank =True)
    available_count =models.IntegerField(null =True,blank =True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)
    fair_price = models.BooleanField(default=True,null =True,blank =True)
    valid_seller = models.BooleanField(default=True,null =True,blank =True)
    is_active=models.BooleanField(default=True,null=True,blank=True)
    country= models.CharField(max_length=300,blank=True,null=True)




class ServiceFiles(models.Model):
    id = models.AutoField(primary_key=True) 
    file = models.FileField(upload_to='files',)
    service = models.ForeignKey(Service,db_index= True , on_delete= models.CASCADE)
class ServiceComments(models.Model):
    id = models.AutoField(primary_key=True) 
    comment = models.CharField(max_length = 200)
    user_id = models.IntegerField(null=True,blank=True)
    service = models.ForeignKey(Service,db_index= True , on_delete= models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    reply = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)



class ServiceQuestions(models.Model):
    id = models.AutoField(primary_key=True) 
    question = models.CharField(max_length = 200)
    title = models.CharField(max_length = 200,null=True,blank=True)
    answer = models.CharField(max_length = 200,null=True,blank=True)
    user_id = models.IntegerField(null=True,blank=True)
    service = models.ForeignKey(Service,db_index= True , on_delete= models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class ServiceVotes(models.Model):
    id = models.AutoField(primary_key=True) 
    votes = models.FloatField()
    service = models.ForeignKey(Service,db_index= True , on_delete= models.CASCADE)

class ServiceNegotiate(models.Model):
    id = models.AutoField(primary_key=True) 
    service = models.ForeignKey(Service,db_index= True , on_delete= models.CASCADE)
    phone = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    price = models.IntegerField(null=True,blank=True)
    user_id = models.IntegerField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    description=models.CharField(max_length=700,blank=True,null=True)