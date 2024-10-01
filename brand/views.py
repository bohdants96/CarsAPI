from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from brand.models import Brand
from .serializer import BrandSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_brands(request):
    filters = {
        'name__in': request.GET.getlist('name'),
        'country__in': request.GET.getlist('country'),
    }

    filters = {k: v for k, v in filters.items() if v}

    brands = Brand.objects.filter(**filters).order_by('id')
    serializer = BrandSerializer(brands, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
