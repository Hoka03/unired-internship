from django.core.management.base import BaseCommand
from django.utils import timezone

from decimal import Decimal

from apps.cards.models import Card


class Command(BaseCommand):
    help = "Send fake message to filtered cards (e.g. status='active')"

    def add_arguments(self, parser):
        parser.add_argument(
            "--status", type=str, default="active",
            help="Filter cards by status (default: 'active')"
        )

    def handle(self, *args, **options):
        status = options["status"]
        cards = Card.objects.filter(card_status=status)

        if not cards.exists():
            self.stdout.write(self.style.WARNING(f"⚠️ No cards found with status='{status}'"))
            return

        self.stdout.write(self.style.SUCCESS(f"📨 Found {cards.count()} cards with status='{status}'"))
        for card in cards:
            card_number = str(card.card_number)
            masked_number = f"{card_number[:4]}****{card_number[-4:]}"
            balance = card.balance if isinstance(card.balance, (int, float, Decimal)) else 0
            message = f"Sizning kartangiz {masked_number} aktiv va foydalanishga {balance} UZS mavjud!"

            print(f"[{timezone.now()}] [Telegram bot] ➜ {message}")
