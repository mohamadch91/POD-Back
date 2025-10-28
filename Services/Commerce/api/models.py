from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Commerce(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length = 200,null =True,blank =True)
    year = models.IntegerField(null =True,blank =True)
    weight = models.FloatField(null =True,blank =True)
    dimensions= models.FloatField(null=True,blank=True)
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
    is_active=models.BooleanField(default=True,null=True,blank=True)
    country= models.IntegerField(blank=True,null=True)


class CommerceFiles(models.Model):
    id = models.AutoField(primary_key=True) 
    file = models.FileField(upload_to='files')
    default = models.BooleanField(default=False,null=True,blank=True)
    commerce = models.ForeignKey(Commerce,db_index= True , on_delete= models.CASCADE)


class CommerceComments(models.Model):
    id = models.AutoField(primary_key=True) 
    comment = models.CharField(max_length = 200)
    user_id = models.IntegerField(null=True,blank=True)
    commerce = models.ForeignKey(Commerce,db_index= True , on_delete= models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    reply = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

class CommerceQuestions(models.Model):
    id = models.AutoField(primary_key=True) 
    question = models.CharField(max_length = 200)
    title = models.CharField(max_length = 200,null=True,blank=True)
    answer = models.CharField(max_length = 200,null=True,blank=True)
    user_id = models.IntegerField(null=True,blank=True)
    commerce = models.ForeignKey(Commerce,db_index= True , on_delete= models.CASCADE)
    # 0 is default
    # 1 is question accepted
    # 2 question rejected
    # 3 answered
    # 4 answer accepted
    # 5 answer rejected
    status = models.IntegerField(default=0,null=True,blank=True)
    reject_reason = models.CharField(max_length=400, null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    



class CommerceVotes(models.Model):
    id = models.AutoField(primary_key=True) 
    votes = models.FloatField()
    commerce = models.ForeignKey(Commerce,db_index= True , on_delete= models.CASCADE)


class CommerceNegotiate(models.Model):
    id = models.AutoField(primary_key=True) 
    commerce = models.ForeignKey(Commerce,db_index= True , on_delete= models.CASCADE)
    phone = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    price = models.IntegerField(null=True,blank=True)
    user_id = models.IntegerField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    description=models.CharField(max_length=700,blank=True,null=True)

class CommerceNegotiateChat(models.Model):
    id = models.AutoField(primary_key=True)
    negotiate= models.ForeignKey(CommerceNegotiate,db_index=True,on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    user_id = models.IntegerField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
