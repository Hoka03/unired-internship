from django.core.exceptions import ValidationError


def phone_validate(phone_number: str) -> None:
    if not phone_number:
        raise ValidationError("Phone Number cannot be empty!")

    if len(phone_number) != 13 or not phone_number.startswith("+998") or not phone_number[1:].isdigit():
        raise ValidationError(
            "Invalid phone number format, phone number must be: +998(XX)123-45-67",
            code="invalid_phone_format",
            params={"value": phone_number}
        )