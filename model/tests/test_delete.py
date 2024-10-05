import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestDeleteModel:
    def _create_admin(self):
        self.admin = User.objects.create_superuser(
            "admin", "admin@gmail.com", "password"
        )
        self.admin.save()
        self.username = self.admin.username
        self.password = "password"

        return RefreshToken.for_user(self.admin).access_token

    def _create_user(self):
        user = dict(
            username="test",
            email="test@gmail.com",
            password="password",
            confirmed_password="password",
        )
        response = self.client.post(self.create_url, user)
        return response.data["access"]

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
        self.model_id = str(response.data["id"])

    def test_delete_success(self):
        response = self.client.delete(self.model_url + self.model_id)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_not_found(self):
        response = self.client.delete(self.model_url + "999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_models_user(self):
        access_token = self._create_user()
        self._login(access_token)
        response = self.client.delete(self.model_url + self.model_id)
        assert response.status_code == status.HTTP_403_FORBIDDEN
