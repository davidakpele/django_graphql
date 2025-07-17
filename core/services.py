from abc import ABC, abstractmethod
from core.models import User


class UserService(ABC):
    @abstractmethod
    def get_user_by_id(self, id: int) -> User:
        pass
