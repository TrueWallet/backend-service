from factory import Sequence
from factory.django import DjangoModelFactory

from ..models import User


class UserFactory(DjangoModelFactory):
    username = Sequence(lambda n: "john%s" % n)

    class Meta:
        model = User
