from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Commerce(models.Model):

    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length = 200)
    year = models.IntegerField()
    weight = models.IntegerField()
    city_id = models.IntegerField()
    description = models.TextField(max_length =1000)
    user_id =models.IntegerField()
    day_price = models.IntegerField()
    month_price = models.IntegerField()
    code = models.CharField(max_length = 200)
    status = models.BooleanField()
    logistic_price =models.IntegerField()
    free_transport = models.BooleanField()



class CommerceImages(models.Model):
    id = models.AutoField(primary_key=True) 
    image = models.ImageField(upload_to='commerce/images')
    commerce = models.ForeignKey(Commerce,db_index= True , on_delete= models.CASCADE)

class CommerceComments(models.Model):
    id = models.AutoField(primary_key=True) 
    comment = models.CharField(max_length = 200)
    commerce = models.ForeignKey(Commerce,db_index= True , on_delete= models.CASCADE)

class CommerceVotes(models.Model):
    id = models.AutoField(primary_key=True) 
    votes = models.IntegerField(max = 5)
    commerce = models.ForeignKey(Commerce,db_index= True , on_delete= models.CASCADE)
