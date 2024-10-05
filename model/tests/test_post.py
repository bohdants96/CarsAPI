import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestPostModel:
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

    def test_post_models_success(self):
        response = self.client.post(self.model_url, self.model, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        assert response.data["name"] == self.model["name"]
        assert response.data["issue_year"] == self.model["issue_year"]
        assert response.data["body_style"] == self.model["body_style"]

    def test_post_models_fail(self):
        model = self.model
        model.pop("body_style")
        response = self.client.post(self.model_url, self.model, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_models_fail_year(self):
        model = self.model
        model["issue_year"] = 1800
        response = self.client.post(self.model_url, self.model, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_models_user(self):
        access_token = self._create_user()
        self._login(access_token)
        response = self.client.post(self.model_url, self.model, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
