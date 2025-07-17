from abc import ABC, abstractmethod
from core.models import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: int) -> User:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass
