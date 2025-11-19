from django.core.exceptions import ValidationError


def phone_validate(phone_number: str):
    if not phone_number:
        raise ValidationError("Phone Number cannot be empty!")

    if len(phone_number) != 13 or not phone_number.startswith("+998") or not phone_number[1:].isdigit():
        raise ValidationError(
            "Invalid phone number format, phone number must be: +998(XX)123-45-67",
            code="invalid_phone_format",
            params={"value": phone_number}
        )


def phone_masK(phone_number: str):
    if not phone_number or not phone_number.startswith("+998"):
        return "(Hidden)"

    if len(phone_number) != 13:
        return "Invalid"

    return f"+998 (**) ***-**{phone_number[-2:]}"


def normalize_phone_number(phone_number: str | None) -> str | None:
    """
    Exceldan kelayotgan phone_number qiymatini normalize qiladi.
    - 998901234567 --> +998901234567
    - 901234567    --> +998901234567
    - +998901234567 --> +998901234567
    """
    if not phone_number or phone_number.strip().lower() in ("", "none", "nan"):
        return None

    phone_number = phone_number.strip().replace(" ", "")

    if phone_number.startswith("+998") and len(phone_number) == 13:
        return phone_number

    if phone_number.startswith("998") and len(phone_number) == 12:
        return f"+{phone_number}"

    if len(phone_number) == 9 and phone_number.isdigit():
        return f"+998{phone_number}"

    raise ValidationError(
        "Phone number is not in a valid format. Expected formats: 901234567 or 998901234567 or +998901234567"
    )