import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestPutCar:
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
        response = self.client.post(self.car_url, self.car, format="json")
        self.car_id = str(response.data["id"])

    def test_put_cars_success(self):
        car = self.car
        car["interior_color"] = "black"
        response = self.client.put(
            self.car_url + self.car_id, car, format="json"
        )
        assert response.status_code == status.HTTP_200_OK

        assert response.data["model"] == self.model["name"]
        assert response.data["interior_color"] == "black"
        assert response.data["brand"] == self.brand["name"]

    def test_put_cars_fail(self):
        car = self.car
        car["price"] = -10000
        response = self.client.put(
            self.car_url + self.car_id, car, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_put_not_found(self):
        car = self.car
        car["interior_color"] = "black"
        response = self.client.put(self.car_url + "999", car, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_put_cars_user(self):
        access_token = self._create_user()
        self._login(access_token)
        car = self.car
        car["interior_color"] = "black"
        response = self.client.put(
            self.car_url + self.car_id, car, format="json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_method_not_allow(self):
        access_token = self._create_user()
        self._login(access_token)
        response = self.client.patch(
            self.car_url + self.car_id, self.car, format="json"
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
