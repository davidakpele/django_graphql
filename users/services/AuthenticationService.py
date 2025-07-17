import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .JwtAuthenticationService import decode_access_token
from graphql import GraphQLError

User = get_user_model() 


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None
        try:
            prefix, token = auth_header.split()
            if prefix.lower() != 'bearer':
                raise AuthenticationFailed({
                    "status": 401,
                    "title": "Authentication Error",
                    "detail": "Invalid token format",
                    "code": "invalid_token"
                })
        except ValueError:
            raise AuthenticationFailed({
                "status": 401,
                "title": "Authentication Error",
                "detail": "Invalid Authorization header",
                "code": "invalid_token"
            })
        user_id = decode_access_token(token)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed({
                "status": 401,
                "title": "Authentication Error",
                "detail": "User not found",
                "code": "invalid_token"
            })
        return (user, None)
    
    def resolve(self, next, root, info, **kwargs):
        request = info.context
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            authenticator = CustomJWTAuthentication()
            user_auth_tuple = authenticator.authenticate(request)
            if user_auth_tuple is None:
                raise GraphQLError("Authentication credentials were not provided.")
            request.user = user_auth_tuple[0]

        return next(root, info, **kwargs)
