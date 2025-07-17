from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from users.graphql.resolvers import Query
import graphene
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import MyTokenObtainPairView
from users.views import RegisterAPI, LoginAPI
from users.views import AuthenticatedGraphQLView

schema = graphene.Schema(query=Query)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
     path("graphql/", csrf_exempt(AuthenticatedGraphQLView.as_view(graphiql=True, schema=schema))),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
