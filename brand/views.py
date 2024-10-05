from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from brand.models import Brand

from .serializer import BrandSerializer


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def manage_brands(request, brand_id=None):
    if request.method == "GET":
        filters = {
            "name__in": request.GET.getlist("name"),
            "country__in": request.GET.getlist("country"),
        }

        filters = {k: v for k, v in filters.items() if v}

        brands = Brand.objects.filter(**filters).order_by("id")
        serializer = BrandSerializer(brands, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if request.user.is_staff:
            serializer = BrandSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
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
                brand = Brand.objects.get(id=brand_id)
                serializer = BrandSerializer(brand, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            except Brand.DoesNotExist:
                return Response(
                    {"detail": "Brand not found."},
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
                brand = Brand.objects.get(id=brand_id)
                brand.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Brand.DoesNotExist:
                return Response(
                    {"detail": "Brand not found."},
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
