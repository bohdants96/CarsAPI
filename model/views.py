from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Model
from .serializer import ModelSerializer


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def manage_models(request, model_id=None):
    if request.method == "GET":
        filters = {
            "name__in": request.GET.getlist("name"),
            "issue_year__in": request.GET.getlist("issue_year"),
            "body_style__in": request.GET.getlist("body_style"),
            "issue_year__gte": request.GET.get("issue_year_min"),
            "issue_year__lte": request.GET.get("issue_year_max"),
        }
        filters = {k: v for k, v in filters.items() if v}

        models = Model.objects.filter(**filters).order_by("id")
        serializer = ModelSerializer(models, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if request.user.is_staff:
            serializer = ModelSerializer(data=request.data)
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
                model = Model.objects.get(id=model_id)
                serializer = ModelSerializer(model, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            except Model.DoesNotExist:
                return Response(
                    {"detail": "Model not found."},
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
                model = Model.objects.get(id=model_id)
                model.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Model.DoesNotExist:
                return Response(
                    {"detail": "Model not found."},
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
