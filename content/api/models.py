from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class NewsCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    summary = models.TextField(max_length=1000,null=True,blank=True)
    image = models.ImageField(upload_to='images')
    category = models.ForeignKey(NewsCategory,db_index= True , on_delete= models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)
    tag= ArrayField(models.CharField(max_length=200), blank=True, null=True)
    resources= ArrayField(models.CharField(max_length=200), blank=True, null=True)

    # status 0 is for defualt ,
    # status 1 is for pending,
    # status 2 is for accepted,
    # status 3 is for rejected,


class NewsImages(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images')
    news = models.ForeignKey(News,db_index= True , on_delete= models.CASCADE)


class BannerCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='images')
    category = models.ForeignKey(BannerCategory,db_index= True , on_delete= models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)
    # status 0 is for defualt ,
    # status 1 is for pending,
    # status 2 is for accepted,
    # status 3 is for rejected,
    link = models.CharField(max_length=200)
    # link to the page that banner should redirect to
    # if link is empty banner will not be clickable



