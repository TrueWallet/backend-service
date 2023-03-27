from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = "auth_api"

urlpatterns = [
    path("obtain/", TokenObtainPairView.as_view(), name="obtain_token"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("verify/", TokenVerifyView.as_view(), name="verify_token"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
]
