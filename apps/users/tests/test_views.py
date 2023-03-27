from unittest.mock import patch

from django.test import override_settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView, TokenVerifyView


@override_settings(TELEGRAM_BOT_TOKEN="42:TEST")  # nosec B106
class TokenObtainPairViewTestCase(APITestCase):
    url = reverse("auth_api:obtain_token")
    data = {"auth_data": "auth-data"}

    @patch.object(TokenObtainPairView, "post", return_value=Response())
    def test_view_url_is_resolved(self, mock_view):
        self.assertEqual(self.url, "/api/v1/auth/obtain/")
        response = self.client.post(self.url, self.data)
        self.assertTrue(mock_view.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TokenRefreshViewTestCase(APITestCase):
    url = reverse("auth_api:refresh_token")
    data = {"refresh": "refresh-token", "access": "access-token"}

    @patch.object(TokenRefreshView, "post", return_value=Response())
    def test_view_url_is_resolved(self, mock_view):
        self.assertEqual(self.url, "/api/v1/auth/refresh/")
        response = self.client.post(self.url, self.data)
        self.assertTrue(mock_view.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TokenVerifyViewTestCase(APITestCase):
    url = reverse("auth_api:verify_token")
    data = {"token": "verify-token"}

    @patch.object(TokenVerifyView, "post", return_value=Response())
    def test_view_url_is_resolved(self, mock_view):
        self.assertEqual(self.url, "/api/v1/auth/verify/")
        response = self.client.post(self.url, self.data)
        self.assertTrue(mock_view.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TokenBlacklistViewTestCase(APITestCase):
    url = reverse("auth_api:logout")
    data = {"refresh": "refresh-token"}

    @patch.object(TokenBlacklistView, "post", return_value=Response())
    def test_view_url_is_resolved(self, mock_view):
        self.assertEqual(self.url, "/api/v1/auth/logout/")
        response = self.client.post(self.url, self.data)
        self.assertTrue(mock_view.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
