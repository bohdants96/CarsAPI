import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestGetCar:
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

        self.model = {"name": "M5", "issue_year": 2020, "body_style": "sedan"}
        self.brand = {"name": "BMW", "country": "Germany"}

        self.model_url = reverse("get_models")
        self.brand_url = reverse("get_brands")
        self.login_url = reverse("login_user")
        self.create_url = reverse("create_user")
        self.car_url = reverse("get_sale_car")

        response = self.client.post(self.brand_url, self.brand, format="json")
        self.brand_id = response.data["id"]

        response = self.client.post(self.model_url, self.model, format="json")
        self.model_id = response.data["id"]

        self.car = {
            "brand_id": self.brand_id,
            "model_id": self.model_id,
            "price": 10000,
            "mileage": 150000,
            "exterior_color": "red",
            "interior_color": "red",
            "fuel_type": "Gas",
            "transmission": "Manual",
            "engine": "2.0L",
            "is_on_sale": 1,
        }
        response = self.client.post(self.car_url, self.car, format="json")
        self.car_id = response.data["id"]

    def test_get_cars_success(self):
        response = self.client.get(self.car_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == self.car_id
        assert type(response.data) == ReturnList

    def test_get_all_cars_success(self):
        response = self.client.get(self.car_url + "all/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["id"] == self.car_id
        assert type(response.data) == ReturnList
