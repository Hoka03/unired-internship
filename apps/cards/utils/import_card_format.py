import re
from django.core.exceptions import ValidationError

def normalize_card_number(card_number: str) -> str:
    digits = re.sub(r"\D", "", card_number)
    if len(digits) != 16:
        raise ValidationError(f"Card number must be 16 digits (got: {card_number})")
    return digits