import genericpath
from django.shortcuts import render
import json
import jwt
from rest_framework.views import APIView
from .models import User_details,User_info
from .serializers import USER_Serializer,Userinfoserializer
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .backends import EmailBackend
from datetime import datetime, timedelta
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from bson import ObjectId
from .permissions import CustomIsauthenticated
JWT_SECRET_KEY = 'django-insecure-@k_ao&*k_1n4b%r(o_%zr^_@y(6@@dw^3q_8jp04*7h*g)mp85'
JWT_ACCESS_TOKEN_EXPIRATION = 120
JWT_REFRESH_TOKEN_EXPIRATION = 1440
JWT_ALGORITHM = 'HS256'


class Register(APIView):
    """
    Allows user to register with unexcited email_id
    """
    
    def post(self, request, format=None):
        serializer = USER_Serializer(data=json.loads(request.body))
        if serializer.is_valid():
            data = serializer.validated_data
            password = data['password'] # Replace "my_password" with the actual password value
            hased_password = make_password(password)   #  the make_password function is actually used to securely hash passwords
            email = data['email']
            existing_user = User_details.objects.filter(email=email).first() # is used to check if a user with a given email address already exists in the" User_details" model
            if existing_user is not None:
                return JsonResponse({'Message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(password=hased_password)
                return JsonResponse({'Message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'Message': 'User not created'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    Allows to login into page with valid credentials and generate valid JWT tokens
    """
    def post(self,request):
        data = request.data
        email = data.get('email',None)
        password = data.get('password',None)
        user=EmailBackend.authenticate(self, request, username=email, password=password) # verifying the user is authenticate or not 
        if user is not None:
            token_payload = {
                'user_id': str(user.id),
                'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRATION)
                }
            # print(user._id)
            access_token = jwt.encode(token_payload, JWT_SECRET_KEY, JWT_ALGORITHM) # generating access_token to the respective user 

            refresh_token_payload = {
                'user_id': str(user.id),
                'exp': datetime.utcnow() + timedelta(days=JWT_REFRESH_TOKEN_EXPIRATION)
                }
            refresh_token = jwt.encode(refresh_token_payload, JWT_SECRET_KEY, JWT_ALGORITHM)# generating refresh_token to the respective user 
    

            return JsonResponse({
                    "status": "success",
                    "message": "user successfully authenticated",
                    "token": access_token.decode("utf-8") ,
                    "refresh_token": refresh_token.decode("utf-8") 
                })
        else:
            return JsonResponse({"message":"invalid data"})



class User_info_view(APIView):
    permission_classes=[CustomIsauthenticated]
    """
    Allows access only to authenticated users with valid JWT tokens.
    """
    def post(self, request):
        serializer = Userinfoserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'user created successfully'})
        return Response({'status': 400, 'payload': serializer.errors})
    
    def get(self,request,pk=None, format=None):
        id=pk
        if id is not None:
            try:
                user = User_info.objects.get(id=pk)
                serializer = Userinfoserializer(user)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except user.DoesNotExist:
                return Response({'Message':"Data is not found "})
        else:
            user = User_info.objects.all()
            serializer = Userinfoserializer(user, many=True)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        
