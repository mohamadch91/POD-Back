from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Service(models.Model):

    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length = 200)
    year = models.IntegerField()
    weight = models.IntegerField()
    city_id = models.IntegerField()
    description = models.TextField(max_length =500)
    user_id =models.IntegerField()
    day_price = models.IntegerField()
    month_price = models.IntegerField()
    code = models.CharField(max_length = 200)
    status = models.BooleanField()
    logistic_price =models.IntegerField()
    free_transport = models.BooleanField()
    discount = models.IntegerField()
    category = models.IntegerField()
    brand = models.IntegerField()
    available_count =models.IntegerField()





class ServiceImages(models.Model):
    image = models.ImageField(upload_to='service/images')
    service = models.ForeignKey(Service,db_index= True , on_delete= models.CASCADE)
class ServiceComments(models.Model):
    id = models.AutoField(primary_key=True) 
    comment = models.CharField(max_length = 200)
    service = models.ForeignKey(Service,db_index= True , on_delete= models.CASCADE)

class ServiceVotes(models.Model):
    id = models.AutoField(primary_key=True) 
    votes = models.IntegerField()
    service = models.ForeignKey(Service,db_index= True , on_delete= models.CASCADE)
