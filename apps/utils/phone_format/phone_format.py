import re

from django.core.exceptions import ValidationError


def phone_validate(phone_number: str):
    if not phone_number:
        raise ValidationError("Phone Number cannot be empty!")

    clean = re.sub(r"[^\d]", "", phone_number)

    if not clean.startswith("998") or len(clean) != 12:
        raise ValidationError(
            "Invalid phone number format, phone number must be: +998(XX)123-45-67",
            code="invalid_phone_format",
            params={"value": phone_number}
        )


def phone_masK(phone_number: str):
    clean = re.sub(r"[^\d]", "", phone_number)

    if not clean.startswith("998") or len(clean) != 12:
        return "Invalid"

    return f"+998 (**) ***-**{clean[-2:]}"


def normalize_phone_number(phone_number: str | None) -> str | None:
    """
    Har qanday formatdagi telefon raqamni faqat sonlarga aylantirib,
    +998 bilan boshlanuvchi standart formatga o'tkazadi.
    """
    if not phone_number or phone_number.strip().lower() in ("", "none", "nan"):
        return None

    # Faqat raqamlarni qoldiramiz
    digits_only = re.sub(r"[^\d]", "", phone_number)

    # 998 bilan boshlanadigan 12 xonali format
    if digits_only.startswith("998") and len(digits_only) >= 12:
        return f"+{digits_only[:12]}"

    # 9 xonali (mahalliy) format
    if len(digits_only) == 9:
        return f"+998{digits_only}"

    raise ValidationError(f"Invalid phone number format: {phone_number}")