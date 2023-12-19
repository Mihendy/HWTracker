from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_extended_slug(value):
    if not value.isalnum() and "_" not in value and "-" not in value:
        raise ValidationError(_("Enter a valid “slug” consisting of letters, numbers, underscores or hyphens."))
