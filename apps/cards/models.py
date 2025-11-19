from django.db import models

from apps.base.models import AbstractBaseModel
from apps.cards.utils.balance_format import format_balance
from apps.cards.utils.card_format import card_number_validate
from apps.cards.utils.expire_format import format_expire
from apps.cards.utils.phone_format import phone_validate


class Card(AbstractBaseModel):
    class CardStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "InActive"
        EXPIRED = "expired", "Expired"

    card_status = models.CharField(
        choices=CardStatus.choices,
        max_length=25,
        help_text="Select the type of card being registered."
    )
    card_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[card_number_validate],
        help_text="Enter the card number using only digits, no spaces or dashes."
    )
    expire = models.CharField(
        max_length=10,
        help_text="Enter the expiry date in MM/YY format."
    )
    phone_number = models.CharField(
        max_length=20,
        validators=[phone_validate],
        blank=True,
        help_text="Enter the phone number with country code, e.g., +998901234567."
    )
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        validators=[format_balance],
        help_text="Here view balance of card,, e.g,."
    )

    def __str__(self):
        return self.card_number

    def clean(self):
        self.expire = format_expire(self.expire)
