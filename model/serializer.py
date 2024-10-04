import django_filters
from rest_framework import serializers

from .models import Model


class ModelSerializer(serializers.ModelSerializer):
    issue_year = django_filters.RangeFilter(field_name="issue_year")

    class Meta:
        model = Model
        fields = "__all__"
