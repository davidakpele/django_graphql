from typing import Optional
from django.contrib.auth import authenticate, get_user_model
from core.models import User as DomainUser
from core.repositories import UserRepository
from core.services import UserService

DjangoUserModel = get_user_model()


class DjangoUserRepository(UserRepository):
    def find_by_id(self, id: int) -> Optional[DomainUser]:
        print(f"Looking for user with id: {id}")  # DEBUG
        try:
            obj = DjangoUserModel.objects.get(pk=id)
            print("User found:", obj.email)  # DEBUG
            # never expose hashed pw
            return DomainUser(id=obj.id, email=obj.email, password="")
        except DjangoUserModel.DoesNotExist:
            print("User not found")  # DEBUG
            return None

    def save(self, user: DomainUser) -> DomainUser:
        # Use manager to ensure password hashing & defaults
        obj = DjangoUserModel.objects.create_user(
            email=user.email,
            password=user.password or None,
        )
        return DomainUser(id=obj.id, email=obj.email, password="")

    def authenticate_user(self, email: str, password: str) -> Optional[DomainUser]:
        # ModelBackend uses USERNAME_FIELD (email in your CustomUser), so pass as username=
        auth_user = authenticate(username=email, password=password)
        if auth_user is None:
            return None
        return DomainUser(id=auth_user.id, email=auth_user.email, password="")


class DjangoUserService(UserService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, id: int) -> Optional[DomainUser]:
        return self.user_repository.find_by_id(id)

    def authenticate(self, email: str, password: str) -> Optional[DomainUser]:
        return self.user_repository.authenticate_user(email, password)
