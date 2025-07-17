import graphene
from graphene_django.types import DjangoObjectType
from users.models import CustomUser  

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser 
        fields = ("id", "email", "firstname",
                  "lastname", "enabled", "createdAt")
    
    @staticmethod
    def resolve_reference(root, info, **kwargs):
        return CustomUser.objects.get(id=kwargs.get("id"))

class CreateUserInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    firstname = graphene.String()
    lastname = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = CreateUserInput(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, input):
        user = CustomUser(
            email=input.email,
            firstname=input.firstname,
            lastname=input.lastname,
        )
        user.set_password(input.password)
        user.save()
        return CreateUser(user=user)
