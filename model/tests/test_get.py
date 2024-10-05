import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestGetModel:
    def _create_admin(self):
        self.admin = User.objects.create_superuser(
            "admin", "admin@gmail.com", "password"
        )
        self.admin.save()
        self.username = self.admin.username
        self.password = "password"

        return RefreshToken.for_user(self.admin).access_token

    def _login(self, access_token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    @pytest.fixture(autouse=True)
    def initialize(self):
        self.client = APIClient()
        access_token = self._create_admin()
        self._login(access_token)

        self.model = {
            "name": "test",
            "issue_year": 2020,
            "body_style": "sedan",
        }

        self.model_url = reverse("get_models")
        self.login_url = reverse("login_user")
        self.create_url = reverse("create_user")

        response = self.client.post(self.model_url, self.model, format="json")
        self.model_id = response.data["id"]

    def test_get_models_success(self):
        response = self.client.get(self.model_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == self.model_id
        assert type(response.data) == ReturnList
