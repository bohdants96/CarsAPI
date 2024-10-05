import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestPostCar:
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

    def test_post_cars_success(self):
        response = self.client.post(self.car_url, self.car, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        assert response.data["brand"] == self.brand["name"]
        assert response.data["model"] == self.model["name"]

    def test_post_cars_fail(self):
        car = self.car
        car.pop("price")
        response = self.client.post(self.car_url, self.car, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_cars_fail_price(self):
        car = self.car
        car["price"] = -10000
        response = self.client.post(self.car_url, self.car, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_cars_fail_mileage(self):
        car = self.car
        car["mileage"] = -10000
        response = self.client.post(self.car_url, self.car, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_cars_user(self):
        access_token = self._create_user()
        self._login(access_token)
        response = self.client.post(self.car_url, self.car, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
