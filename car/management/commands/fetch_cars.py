from django.core.management.base import BaseCommand
import requests

from brand.models import Brand
from car.models import Car
from model.models import Model

from faker import Faker
import time
from faker_vehicle import VehicleProvider

url = 'https://freetestapi.com/api/v1/cars'
fake = Faker()
Faker.seed(time.time() * 1000)
fake.add_provider(VehicleProvider)


class Command(BaseCommand):
    help = "Fetches Car Objects"

    def add_arguments(self, parser):
        parser.add_argument("count", action="store", nargs="+", default=10, type=int, help="Number of cars to generate")

    def handle(self, *args, **options):
        try:
            count = options["count"][0]
            response = requests.get(f'{url}?limit={count}')
            response.raise_for_status()
            cars_data = response.json()
            for car in cars_data:
                brand, _ = Brand.objects.get_or_create(
                    name=car['make'],
                    country=fake.country()
                )
                model, _ = Model.objects.get_or_create(
                    name=car['model'],
                    issue_year=car['year'],
                    body_style=fake.vehicle_category()
                )

                car = Car(
                    brand=brand,
                    model=model,
                    price=car['price'],
                    mileage=car['mileage'],
                    exterior_color=car['color'],
                    interior_color=car['color'],
                    fuel_type=car['fuelType'],
                    transmission=car['transmission'],
                    engine=car['engine'],
                    is_on_sale=fake.pybool(),
                )
                car.save()
            return self.stdout.write("done")
        except Exception as e:
            self.stdout.write(e)
