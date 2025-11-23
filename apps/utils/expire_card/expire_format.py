import re

from django.core.exceptions import ValidationError


def format_expire(expire: str):
    if not expire:
        raise ValidationError("Expire cannot be empty!")

    if expire.isalnum():
        raise ValidationError("Expire must be number, for example: 12/24")

    raw_expire = expire.strip()

    raw_expire = re.sub(r"[^0-9]", "/", raw_expire)

    parts = [part for part in raw_expire.split("/") if part]

    if len(parts) != 2:
        raise ValidationError("Format of expire was not correct!! For example:"
                              "12/24 or 12/2024")

    if len(parts[0]) == 4:
        year = parts[0]
        month = parts[1]
    else:
        month = parts[0]
        year = parts[1]

    if len(year) == 4:
        year = year[2:]

    if not (month.isdigit() and year.isdigit()):
        raise ValidationError("Expire must be a number, for example 12/24")

    month_number = int(month)
    if not 1 <= month_number <= 12:
        raise ValidationError("Month must be between 1, 12")

    return f"{month_number}/{year}"