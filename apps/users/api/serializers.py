from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.contrib.auth.models import update_last_login
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from ..exceptions import TelegramWebAppInvalidData
from ..services import TelegramWebAppService, UserService

if TYPE_CHECKING:
    from rest_framework_simplejwt.tokens import Token

    from ..models import User


class TokenObtainPairSerializer(serializers.Serializer):
    token_class = RefreshToken

    auth_data = serializers.CharField()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        data = {}

        try:
            tg_user_data = TelegramWebAppService.safe_parse_webapp_init_data(
                token=settings.TELEGRAM_BOT_TOKEN, init_data=attrs["auth_data"]
            )
        except TelegramWebAppInvalidData:
            raise serializers.ValidationError("Invalid init data signature")

        self.user, _ = UserService.get_or_create(user_tg_id=tg_user_data["user"]["id"])

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(sender=None, user=self.user)  # type: ignore

        return data

    @classmethod
    def get_token(cls, user: "User") -> "Token":
        return cls.token_class.for_user(user)
