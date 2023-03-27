import hashlib
import hmac
import json
from operator import itemgetter
from typing import TYPE_CHECKING, Any, Callable
from urllib.parse import parse_qsl

from .exceptions import TelegramWebAppInvalidData
from .repositories import UserRepository

if TYPE_CHECKING:
    from .models import User


class UserService:
    _user_repo = UserRepository

    @classmethod
    def get_or_create(cls, user_tg_id: str) -> tuple["User", bool]:
        return cls._user_repo.get_or_create(username=user_tg_id)


class TelegramWebAppService:
    @classmethod
    def check_webapp_signature(cls, token: str, init_data: str) -> bool:
        """
        Source: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
        """
        try:
            parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
        except ValueError:  # pragma: no cover
            # Init data is not a valid query string
            return False
        if "hash" not in parsed_data:
            # Hash is not present in init data
            return False
        hash_ = parsed_data.pop("hash")

        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0)))
        secret_key = hmac.new(key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256)
        calculated_hash = hmac.new(
            key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        return calculated_hash == hash_

    @classmethod
    def parse_webapp_init_data(cls, init_data: str, *, loads: Callable[..., Any] = json.loads) -> dict[str, Any]:
        result = {}
        for key, value in parse_qsl(init_data):
            if (value.startswith("[") and value.endswith("]")) or (value.startswith("{") and value.endswith("}")):
                value = loads(value)
            result[key] = value
        return result

    @classmethod
    def safe_parse_webapp_init_data(
        cls, token: str, init_data: str, *, loads: Callable[..., Any] = json.loads
    ) -> dict[str, Any]:
        if cls.check_webapp_signature(token, init_data):
            return cls.parse_webapp_init_data(init_data, loads=loads)
        raise TelegramWebAppInvalidData("Invalid init data signature")
