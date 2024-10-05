import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestPutModel:
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

    def test_put_models_success(self):
        model = self.model
        model["issue_year"] = 2024
        response = self.client.put(
            self.model_url + self.model_id, model, format="json"
        )
        assert response.status_code == status.HTTP_200_OK

        assert response.data["name"] == model["name"]
        assert response.data["issue_year"] == model["issue_year"]
        assert response.data["body_style"] == model["body_style"]

    def test_put_models_fail(self):
        model = self.model
        model["issue_year"] = "fail"
        response = self.client.put(
            self.model_url + self.model_id, model, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_put_not_found(self):
        model = self.model
        model["issue_year"] = 2010
        response = self.client.put(
            self.model_url + "999", model, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_put_models_user(self):
        access_token = self._create_user()
        self._login(access_token)
        model = self.model
        model["issue_year"] = 2010
        response = self.client.put(
            self.model_url + self.model_id, model, format="json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_method_not_allow(self):
        access_token = self._create_user()
        self._login(access_token)
        response = self.client.patch(
            self.model_url + self.model_id, self.model, format="json"
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
