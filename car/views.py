from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from brand.models import Brand
from model.models import Model

from .models import Car
from .serializer import CarSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cars(request):
    filters = {
        "brand__name__in": request.GET.getlist("brand_name"),
        "model__name__in": request.GET.getlist("model_name"),
        "brand__country__in": request.GET.getlist("country"),
        "model__issue_year__in": request.GET.getlist("year"),
        "model__issue_year__gte": request.GET.get("year_min"),
        "model__issue_year__lte": request.GET.get("year_max"),
        "price__gte": request.GET.get("price_min"),
        "price__lte": request.GET.get("price_max"),
        "mileage__gte": request.GET.get("mileage_min"),
        "mileage__lte": request.GET.get("mileage_max"),
        "price__range": (
            (request.GET.get("price_min"), request.GET.get("price_max"))
            if request.GET.get("price_min") and request.GET.get("price_max")
            else None
        ),
        "mileage__range": (
            (request.GET.get("mileage_min"), request.GET.get("mileage_max"))
            if request.GET.get("mileage_min")
            and request.GET.get("mileage_max")
            else None
        ),
        "exterior_color__in": request.GET.getlist("exterior_color"),
        "interior_color__in": request.GET.getlist("interior_color"),
        "fuel_type__in": request.GET.getlist("fuel_type"),
        "transmission__in": request.GET.getlist("transmission"),
        "engine__in": request.GET.getlist("engine"),
    }

    filters = {k: v for k, v in filters.items() if v}

    cars = Car.objects.filter(**filters).order_by("id")
    serializer = CarSerializer(cars, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def manage_sale_car(request, car_id=None):
    if request.method == "GET":
        filters = {
            "brand__name__in": request.GET.getlist("brand_name"),
            "model__name__in": request.GET.getlist("model_name"),
            "brand__country__in": request.GET.getlist("country"),
            "model__issue_year__in": request.GET.getlist("year"),
            "model__issue_year__gte": request.GET.get("year_min"),
            "model__issue_year__lte": request.GET.get("year_max"),
            "price__gte": request.GET.get("price_min"),
            "price__lte": request.GET.get("price_max"),
            "mileage__gte": request.GET.get("mileage_min"),
            "mileage__lte": request.GET.get("mileage_max"),
            "price__range": (
                (request.GET.get("price_min"), request.GET.get("price_max"))
                if request.GET.get("price_min")
                and request.GET.get("price_max")
                else None
            ),
            "mileage__range": (
                (
                    request.GET.get("mileage_min"),
                    request.GET.get("mileage_max"),
                )
                if request.GET.get("mileage_min")
                and request.GET.get("mileage_max")
                else None
            ),
            "exterior_color__in": request.GET.getlist("exterior_color"),
            "interior_color__in": request.GET.getlist("interior_color"),
            "fuel_type__in": request.GET.getlist("fuel_type"),
            "transmission__in": request.GET.getlist("transmission"),
            "engine__in": request.GET.getlist("engine"),
            "is_on_sale": True,
        }

        filters = {k: v for k, v in filters.items() if v}

        cars = Car.objects.filter(**filters).order_by("id")
        serializer = CarSerializer(cars, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if request.user.is_staff:
            data = request.data.copy()
            data["model"] = Model.objects.get(id=data.pop("model_id"))
            data["brand"] = Brand.objects.get(id=data.pop("brand_id"))
            try:
                car = Car(**data)
                car.full_clean()
                car.save()
                serializer = CarSerializer(car)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )

            except Exception as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    "detail": "You do not have permission to perform this action."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    elif request.method == "PUT":
        if request.user.is_staff:
            try:
                car = Car.objects.get(id=car_id)
                try:
                    data = request.data.copy()
                    data["model"] = Model.objects.get(id=data.pop("model_id"))
                    data["brand"] = Brand.objects.get(id=data.pop("brand_id"))
                    for key, value in data.items():
                        setattr(car, key, value)
                    car.full_clean()
                    car.save()
                    serializer = CarSerializer(car)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(e, status=status.HTTP_400_BAD_REQUEST)
            except Car.DoesNotExist:
                return Response(
                    {"detail": "Car not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {
                    "detail": "You do not have permission to perform this action."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    elif request.method == "DELETE":
        if request.user.is_staff:
            try:
                car = Car.objects.get(id=car_id)
                car.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Car.DoesNotExist:
                return Response(
                    {"detail": "Car not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {
                    "detail": "You do not have permission to perform this action."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    return Response(
        {"detail": "Method not allowed."},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )
