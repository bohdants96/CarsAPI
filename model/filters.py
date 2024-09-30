import django_filters
from .models import Model


class ModelFilter(django_filters.FilterSet):
    issue_year = django_filters.RangeFilter(field_name="issue_year")

    class Meta:
        model = Model
        fields = ['issue_year']
