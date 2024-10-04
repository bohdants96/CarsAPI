from django.db import models

from brand.models import Brand
from model.models import Model

from .validators import validate_mileage, validate_price

TRANSMISSION_OPTIONS = (
    ("Manual", "Manual"),
    ("Automatic", "Automatic"),
    ("CVT", "CVT"),
)


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[validate_price])
    mileage = models.IntegerField(validators=[validate_mileage])
    exterior_color = models.CharField(max_length=50)
    interior_color = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    transmission = models.CharField(
        max_length=50, choices=TRANSMISSION_OPTIONS, default="Manual"
    )
    engine = models.CharField(max_length=50)
    is_on_sale = models.BooleanField()

    def __str__(self):
        return self.brand.name + " " + self.model.name

    class Meta:
        ordering = ["price"]
        verbose_name = "car"
        verbose_name_plural = "cars"
