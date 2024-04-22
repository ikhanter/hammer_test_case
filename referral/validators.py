import string
from django.core.exceptions import ValidationError


def validate_phone_number(phone_number: str):
    if not phone_number:
        raise ValueError('Phone number must be provided.')
    if not phone_number.startswith('+'):
        raise ValidationError('Phone number must starts with \'+\' symbol.')
    elif phone_number.startswith('+') and len(phone_number) == 1:
        raise ValidationError('Phone number must contain digits.')
    for el in phone_number[1:]:
        if el not in string.digits:
            raise ValidationError('Phone number must contain only digits.')
