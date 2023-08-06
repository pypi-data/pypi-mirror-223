from rest_framework import serializers
from .models import User_details,User_info

 

class USER_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_details
        fields = ['username','email','password','date_joined']

class Userinfoserializer(serializers.ModelSerializer):
    class Meta:
        model = User_info
        fields = ['username','phone_number','address']