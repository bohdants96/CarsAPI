from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(value):
    if value < 1885 or value > date.today().year:
        raise ValidationError(
            _("%(value)s is not a valid year"),
            params={"value": value},
        )
