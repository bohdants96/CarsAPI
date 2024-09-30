from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from brand.models import Brand
from .serializer import BrandSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_brands(request):
    name = request.GET.getlist('name')
    country = request.GET.getlist('country')

    brands = Brand.objects.all().order_by('id')

    if name:
        brands = brands.filter(name__in=name)
    if country:
        brands = brands.filter(country__in=country)

    serializer = BrandSerializer(brands, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
