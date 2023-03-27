from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory

from ..api.serializers import TokenObtainPairSerializer


@override_settings(TELEGRAM_BOT_TOKEN="42:TEST")  # nosec B106
class TokenObtainPairSerializerTestCase(TestCase):
    request = APIRequestFactory().get("dummy-endpoint")

    def test_success(self):
        data = {
            "auth_data": "auth_date=1650385342"
            "&user=%7B%22id%22%3A42%2C%22first_name%22%3A%22Test%22%7D"
            "&query_id=test"
            "&hash=46d2ea5e32911ec8d30999b56247654460c0d20949b6277af519e76271182803"
        }
        serializer = TokenObtainPairSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertIn("refresh", serializer.validated_data)
        self.assertIn("access", serializer.validated_data)

    def test_invalid_data(self):
        data = {
            "auth_data": "auth_date=1650385342"
            "&user=%7B%22id%22%3A42%2C%22first_name%22%3A%22Test%22%7D"
            "&query_id=test"
            "&hash=test"
        }
        serializer = TokenObtainPairSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {"non_field_errors": ["Invalid init data signature"]})
