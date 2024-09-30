from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    model = serializers.StringRelatedField()

    class Meta:
        model = Car
        fields = [
            "id",
            "brand",
            "model",
            "price",
            "mileage",
            "exterior_color",
            "interior_color",
            "fuel_type",
            "transmission",
            "engine",
            "is_on_sale",
        ]
