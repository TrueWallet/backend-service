from .models import User


class UserRepository:
    _model = User

    @classmethod
    def get_or_create(cls, username: str) -> tuple[User, bool]:
        return cls._model.objects.get_or_create(username=username)
