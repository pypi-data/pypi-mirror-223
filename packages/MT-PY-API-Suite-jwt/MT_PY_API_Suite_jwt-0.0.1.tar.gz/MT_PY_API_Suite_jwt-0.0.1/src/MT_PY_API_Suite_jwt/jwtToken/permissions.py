import jwt
from rest_framework.permissions import IsAuthenticated
from .models import User_details
from rest_framework.exceptions import AuthenticationFailed
from bson import ObjectId
JWT_SECRET_KEY = 'django-insecure-@k_ao&*k_1n4b%r(o_%zr^_@y(6@@dw^3q_8jp04*7h*g)mp85'
JWT_ACCESS_TOKEN_EXPIRATION = 120
JWT_REFRESH_TOKEN_EXPIRATION = 1440
JWT_ALGORITHM = 'HS256'


class CustomIsauthenticated(IsAuthenticated):
    """
    Allows access only to authenticated users with valid JWT tokens.
    """

    def has_permission(self, request, view):
        try:
            import pdb;pdb.set_trace
            auth_header = request.headers['Authorization']
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            print(payload)
            user = User_details.objects.get(id=payload['user_id'])
           
            return True
        except (KeyError, jwt.exceptions.DecodeError, User_details.DoesNotExist):
            raise AuthenticationFailed({'message': 'Authorization details are not provided'})

