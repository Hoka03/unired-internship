from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError


def format_balance(value):
    """
    Validates that balance is a valid number between 1 and 1,200,000,000 (UZS).
    Must be a positive decimal with max 2 decimal places.
    """

    if value in [None, ""]:
        raise ValidationError("Balance cannot be empty.")

    try:
        balance = Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        raise ValidationError("Balance must be a valid number.")

    if balance <= 0:
        raise ValidationError("Balance must be greater than 0.")

    if balance > Decimal("1200000000"):
        raise ValidationError("Balance cannot exceed 1.2 billion UZS.")

    if balance.as_tuple().exponent < -2:
        raise ValidationError("Balance cannot have more than 2 decimal places.")


def clean_balance_value(raw_balance):
    """Excel'dan kelgan balance qiymatini Decimal ga aylantiradi"""
    if raw_balance in (None, "", " "):
        return Decimal("0")

    try:
        return Decimal(str(raw_balance).strip().replace(",", "").replace(" ", ""))
    except (InvalidOperation, ValueError, TypeError):
        raise ValidationError("Balance must be a valid number.")