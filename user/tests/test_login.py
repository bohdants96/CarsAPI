import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestLogin:

    def _create_user(self, client):
        user = dict(
            username="admin",
            email="admin@gmail.com",
            password="password",
            confirmed_password="password",
        )
        create_url = reverse("create_user")
        client.post(create_url, user)

    @pytest.fixture(autouse=True)
    def initialize(self):
        self.client = APIClient()
        self.user_success = dict(
            username="admin",
            password="password",
        )
        self.user_fail = dict(
            username="admin",
            password="password_fail",
        )

        self.login_url = reverse("login_user")

    def test_login_success(self, client):
        self._create_user(client)
        response = client.post(self.login_url, self.user_success)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["access"]
        assert response.data["refresh"]

    def test_login_fail(self, client):
        self._create_user(client)
        response = client.post(self.login_url, self.user_fail)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_username_fail(self, client):
        self._create_user(client)
        user = self.user_success
        user["username"] = "fail"
        response = client.post(self.login_url, self.user_fail)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
