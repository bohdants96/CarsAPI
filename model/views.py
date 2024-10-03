from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Model
from .serializer import ModelSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_models(request):
    filters = {
        'name__in': request.GET.getlist('name'),
        'issue_year__in': request.GET.getlist('issue_year'),
        'body_style__in': request.GET.getlist('body_style'),
        'issue_year__gte': request.GET.get('issue_year_min'),
        'issue_year__lte': request.GET.get('issue_year_max'),
    }

    filters = {k: v for k, v in filters.items() if v}

    models = Model.objects.filter(**filters).order_by('id')
    serializer = ModelSerializer(models, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
