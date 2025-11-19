import re
from django.core.exceptions import ValidationError


def card_number_validate(card_number: str):
    if not card_number:
        raise ValidationError("Card Number cannot be empty!")

    clean_card_number = re.sub(r"[ \-,.]", "", card_number)

    if not clean_card_number.isdigit():
        raise ValidationError(
            f"Invalid card number: card number must be only digits (got: {card_number})"
        )

    if len(card_number) != 16:
        raise ValidationError(
            f"Card number must be 16 digits (got: {card_number})"
        )

    card_valid_prefix = ("8600", "5614", "5440", "4003", "9860")
    if not clean_card_number.startswith(card_valid_prefix):
        raise ValidationError(
            f"Invalid card number prefix (got: {card_number})"
        )

    return clean_card_number