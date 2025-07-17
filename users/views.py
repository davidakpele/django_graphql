from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import json
from graphene_django.views import GraphQLView
from .models import CustomUser
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .services.JwtAuthenticationService import create_access_token, create_refresh_token
from .services.AuthenticationService import CustomJWTAuthentication

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email' 

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    def validate(self, attrs):
        attrs['username'] = attrs.pop('email')
        return super().validate(attrs)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer  # ✅ Only this

# 🔒 Secure GraphQL with JWT
class AuthenticatedGraphQLView(GraphQLView):
    def parse_body(self, request):
        auth = CustomJWTAuthentication()
        user_auth_tuple = auth.authenticate(request)

        if not user_auth_tuple:
            return JsonResponse({'error': 'Authentication credentials were not provided'}, status=401)

        request.user = user_auth_tuple[0]
        return super().parse_body(request)
        

class RegisterAPI(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            # Validate email
            if not email or email.strip() == '':
                return JsonResponse({'error': 'Email cannot be empty or null.', 'status': 400}, status=400)

            # Validate password
            if not password or password.strip() == '':
                return JsonResponse({'error': 'Password cannot be empty or null.', 'status': 400}, status=400)

            # Check if email already exists
            user = CustomUser.objects.filter(email=email).first()
            if user is not None:
                return JsonResponse({'error': 'User already taken this email address.*', 'status': 409}, status=409)

            # Create user
            user = CustomUser.objects.create_user(
                email=email,
                password=password
            )
            user.enabled = False
            user.save()

            return JsonResponse({'message': 'Account has been successfully registered.!.', 'status': 201}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data', 'status': 400}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 500}, status=500)


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            # Validate email and password
            if not email or email.strip() == '':
                return JsonResponse({'error': 'Email cannot be empty or null.', 'status': 400}, status=400)
            if not password or password.strip() == '':
                return JsonResponse({'error': 'Password cannot be empty or null.', 'status': 400}, status=400)

            # Authenticate user
            user = authenticate(email=email, password=password)
            if user is None:
                return JsonResponse({'error': 'Invalid email or password.', 'status': 401}, status=401)

            # Set session
            request.session['email'] = user.email

            # Generate tokens
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)

            # Prepare response
            response = Response()
            response.data = {
                'token': access_token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'enabled': user.enabled,
                    'createdAt': user.createdAt,
                },
                'status': 200
            }
            response.set_cookie(
                key='jwt', value=refresh_token, httponly=True, samesite='Lax')
            return response

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data', 'status': 400}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 500}, status=500)
