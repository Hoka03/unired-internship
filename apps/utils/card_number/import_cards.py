import openpyxl

from logging import raiseExceptions

from django.core.exceptions import ValidationError

from apps.cards.models import Card
from apps.utils.expire_card.expire_format import format_expire
from apps.utils.balance.balance_format import clean_balance_value
from apps.utils.phone_format.phone_format import normalize_phone_number
from apps.utils.card_number.import_card_format import normalize_card_number


def clean_field(value, func, field_name, row_index):
    try:
        return func(value)
    except ValidationError as e:
        raise ValidationError(f"{field_name} error in row {row_index}: {e}")


def import_cards_from_excel(file_obj) -> dict:
    wb = openpyxl.load_workbook(file_obj)
    ws = wb.active

    created_count = 0
    updated_count = 0
    errors = []

    for i, row in enumerate(ws.iter_rows(min_row=2), start=2):
        try:
            raw_card_number = str(row[0].value).strip() if row[0].value else ""
            raw_expire = str(row[1].value).strip() if row[1].value else ""
            raw_phone = str(row[2].value).strip() if row[2].value else ""
            raw_status = str(row[3].value).strip().lower() if row[3].value else raiseExceptions
            raw_balance = row[4].value

            cleaned_card_number = normalize_card_number(raw_card_number)
            cleaned_phone = normalize_phone_number(raw_phone)
            cleaned_expire = format_expire(raw_expire)
            cleaned_balance = clean_balance_value(raw_balance)

            if raw_status in ["active", "inactive", "expired"]:
                cleaned_status = raw_status
            else:
                raise ValidationError(f"Card status '{raw_status}' is not valid")

            card, created = Card.objects.update_or_create(
                card_number=cleaned_card_number,
                defaults={
                    "expire": cleaned_expire,
                    "phone_number": cleaned_phone,
                    "balance": cleaned_balance,
                    "card_status": cleaned_status
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        except ValidationError as e:
            errors.append(f"Row {i}: {e.messages}")
        except Exception as e:
            errors.append(f"Row {i}: {str(e)}")

    return {
        "created": created_count,
        "updated": updated_count,
        "errors": errors
    }
