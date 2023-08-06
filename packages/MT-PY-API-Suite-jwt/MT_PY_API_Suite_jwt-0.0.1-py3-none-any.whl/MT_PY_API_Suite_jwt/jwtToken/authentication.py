import jwt
from .models import User_details
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from bson import ObjectId
JWT_SECRET_KEY = 'django-insecure-@k_ao&*k_1n4b%r(o_%zr^_@y(6@@dw^3q_8jp04*7h*g)mp85'
JWT_ACCESS_TOKEN_EXPIRATION = 120
JWT_REFRESH_TOKEN_EXPIRATION = 1440
JWT_ALGORITHM = 'HS256'
        
class JWTAuthentication(BaseAuthentication):
    """
    Allows access only to authenticated users with valid JWT tokens.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        try:
            _, token = auth_header.split()
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except (ValueError, jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            raise AuthenticationFailed('Invalid token.')
        try:
            user = User_details.objects.get(id=payload['user_id'])
        except User_details.DoesNotExist:
            raise AuthenticationFailed('User not found.')
        return (user, None)
    