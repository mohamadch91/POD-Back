from django.db import models

# Create your models here.


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    products_data =models.JSONField()
    amount = models.IntegerField()
    status = models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

