import time

from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import DynamicProvider
from faker_vehicle import VehicleProvider

from brand.models import Brand
from car.models import Car
from model.models import Model

fake = Faker()
Faker.seed(time.time() * 1000)
fake.add_provider(VehicleProvider)

fuel_type_provider = DynamicProvider(
    provider_name="fuel_type",
    elements=["Gasoline", "Diesel Fuel", "Electric"],
)
fake.add_provider(fuel_type_provider)

transmission_provider = DynamicProvider(
    provider_name="transmission", elements=["Manual", "Automatic", "CVT"]
)
fake.add_provider(transmission_provider)

engine_provider = DynamicProvider(
    provider_name="engine", elements=["2.0L", "1.4L", "3.0L", "5.0L"]
)
fake.add_provider(engine_provider)


class Command(BaseCommand):
    help = "Generates Car Objects"

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            action="store",
            nargs="+",
            default=10,
            type=int,
            help="Number of cars to generate",
        )

    def handle(self, *args, **options):
        count = options["count"][0]
        for _ in range(count):
            car_data = fake.vehicle_object()
            brand_example, _ = Brand.objects.get_or_create(
                name=car_data["Make"], country=fake.country()
            )
            model_example, _ = Model.objects.get_or_create(
                name=car_data["Model"],
                issue_year=car_data["Year"],
                body_style=car_data["Category"],
            )

            car = Car(
                brand=brand_example,
                model=model_example,
                price=fake.pyint(),
                mileage=fake.pyint(),
                exterior_color=fake.color(),
                interior_color=fake.color(),
                fuel_type=fake.fuel_type(),
                transmission=fake.transmission(),
                engine=fake.engine(),
                is_on_sale=fake.pybool(),
            )
            car.save()
        return self.stdout.write("done")
