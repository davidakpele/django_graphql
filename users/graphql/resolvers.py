import graphene
from graphene_federation import build_schema, key
from users.adapters import DjangoUserRepository, DjangoUserService
from users.models import CustomUser  # <- Updated
from users.graphql.schema import CreateUser

@key(fields="id")
class UserType(graphene.ObjectType):
    id = graphene.ID()
    email = graphene.String()

    @staticmethod
    def resolve_reference(root, info, **kwargs):
        return CustomUser.objects.get(id=kwargs.get("id"))


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_user(self, info, id):
        repo = DjangoUserRepository()
        user = repo.find_by_id(id)
        return user if user else None


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = build_schema(
    query=Query,
    mutation=Mutation,
    types=[UserType],
)
