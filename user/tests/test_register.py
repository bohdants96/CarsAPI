import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestRegister:

    @pytest.fixture(autouse=True)
    def initialize(self):
        self.client = APIClient()
        self.user = dict(
            username="admin",
            email="admin@gmail.com",
            password="password",
            confirmed_password="password",
        )

        self.bad_user = dict(
            username="",
            email="email",
            password="password",
            confirmed_password="password_dont_match",
        )

        self.create_url = reverse("create_user")

    def test_register_user_success(self, client):
        response = client.post(self.create_url, self.user)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["access"]
        assert response.data["refresh"]

    def test_register_user_match_password(self, client):
        user_dont_match_password = self.user
        user_dont_match_password["confirmed_password"] = "dont_match_password"
        response = client.post(self.create_url, user_dont_match_password)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_bad_user(self, client):
        response = client.post(self.create_url, self.bad_user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
