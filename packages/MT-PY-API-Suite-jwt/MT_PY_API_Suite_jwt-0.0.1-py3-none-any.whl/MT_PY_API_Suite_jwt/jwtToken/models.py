from django.db import models
from djongo import models
# Create your models here.

class User_details(models.Model):  
    username = models.CharField(max_length=138)
    email = models.EmailField()
    password = models.CharField(max_length=138)
    date_joined = models.DateTimeField(auto_now_add=True)

class User_info(models.Model):
    username =models.CharField(max_length=150)
    phone_number = models.IntegerField()
    address =models.CharField(max_length=300)

