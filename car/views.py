from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Car
from .serializer import CarSerializer


@api_view(['GET'])
def get_cars(request):
    filters = {
        'brand__name__in': request.GET.getlist('brand_name'),
        'model__name__in': request.GET.getlist('model_name'),
        'brand__country__in': request.GET.getlist('country'),
        'model__issue_year__in': request.GET.getlist('year'),
        'model__issue_year__gte': request.GET.get('year_min'),
        'model__issue_year__lte': request.GET.get('year_max'),
        'price__gte': request.GET.get('price_min'),
        'price__lte': request.GET.get('price_max'),
        'mileage__gte': request.GET.get('mileage_min'),
        'mileage__lte': request.GET.get('mileage_max'),
        'price__range': (request.GET.get('price_min'), request.GET.get('price_max')) if request.GET.get(
            'price_min') and request.GET.get('price_max') else None,
        'mileage__range': (request.GET.get('mileage_min'), request.GET.get('mileage_max')) if request.GET.get(
            'mileage_min') and request.GET.get('mileage_max') else None,
        'exterior_color__in': request.GET.getlist('exterior_color'),
        'interior_color__in': request.GET.getlist('interior_color'),
        'fuel_type__in': request.GET.getlist('fuel_type'),
        'transmission__in': request.GET.getlist('transmission'),
        'engine__in': request.GET.getlist('engine'),
    }

    filters = {k: v for k, v in filters.items() if v}

    cars = Car.objects.filter(**filters).order_by('id')
    serializer = CarSerializer(cars, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_sale_cars(request):
    filters = {
        'brand__name__in': request.GET.getlist('brand_name'),
        'model__name__in': request.GET.getlist('model_name'),
        'brand__country__in': request.GET.getlist('country'),
        'model__issue_year__in': request.GET.getlist('year'),
        'model__issue_year__gte': request.GET.get('year_min'),
        'model__issue_year__lte': request.GET.get('year_max'),
        'price__gte': request.GET.get('price_min'),
        'price__lte': request.GET.get('price_max'),
        'mileage__gte': request.GET.get('mileage_min'),
        'mileage__lte': request.GET.get('mileage_max'),
        'price__range': (request.GET.get('price_min'), request.GET.get('price_max')) if request.GET.get(
            'price_min') and request.GET.get('price_max') else None,
        'mileage__range': (request.GET.get('mileage_min'), request.GET.get('mileage_max')) if request.GET.get(
            'mileage_min') and request.GET.get('mileage_max') else None,
        'exterior_color__in': request.GET.getlist('exterior_color'),
        'interior_color__in': request.GET.getlist('interior_color'),
        'fuel_type__in': request.GET.getlist('fuel_type'),
        'transmission__in': request.GET.getlist('transmission'),
        'engine__in': request.GET.getlist('engine'),
        'is_on_sale': True
    }

    filters = {k: v for k, v in filters.items() if v}

    cars = Car.objects.filter(**filters).order_by('id')
    serializer = CarSerializer(cars, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
