from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_price(value):
    if value < 0:
        raise ValidationError(
            _("%(value)s must have a positive value"),
            params={"value": value},
        )


def validate_mileage(value):
    if value < 0:
        raise ValidationError(
            _("%(value)s must have a positive value"),
            params={"value": value},
        )
