from django.db import models

# Create your models here.


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    products_data =models.JSONField()
    order_type = models.CharField(max_length=50)
    amount = models.IntegerField()
    status = models.IntegerField(default=0,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

