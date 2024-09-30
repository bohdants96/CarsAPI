from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Model
from .serializer import ModelSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_models(request):
    name = request.GET.getlist('name')
    issue_year = request.GET.getlist('issue_year')
    body_style = request.GET.getlist('body_style')
    issue_year_min = request.GET.get('issue_year_min')
    issue_year_max = request.GET.get('issue_year_max')

    models = Model.objects.all().order_by('id')

    if name:
        models = models.filter(name__in=name)
    if issue_year:
        models = models.filter(issue_year__in=issue_year)
    if body_style:
        models = models.filter(body_style__in=body_style)

    if issue_year_min and issue_year_max:
        models = models.filter(issue_year__range=(issue_year_min, issue_year_max))
    elif issue_year_min:
        models = models.filter(issue_year__gte=issue_year_min)
    elif issue_year_max:
        models = models.filter(issue_year__lte=issue_year_max)

    serializer = ModelSerializer(models, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
