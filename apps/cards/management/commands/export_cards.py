import csv, os

from django.conf import settings
from django.utils.timezone import datetime
from django.core.management.base import BaseCommand

from apps.cards.models import Card


class Command(BaseCommand):
    help = "Export cards to CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            '--status', type=str, help="Filter by card status (e.g. active, inactive, expired)"
        )
        parser.add_argument(
            '--card_number', type=str, help="Filter by card number (full or partial)"
        )
        parser.add_argument(
            '--phone', type=str, help="Filter by phone number (full or partial)"
        )
        parser.add_argument(
            '--output', type=str, default='exported_cards.csv', help="Output CSV file name"
        )

    def handle(self, *args, **options):
        status = options['status']
        card_number = options['card_number']
        phone = options['phone']
        output_file = options['output']

        today = datetime.now().strftime('%Y%m%d')
        export_dir = os.path.join(settings.BASE_DIR, 'exports', 'cards', today)
        os.makedirs(export_dir, exist_ok=True)

        full_path = os.path.join(export_dir, output_file)

        queryset = Card.objects.all()
        if status:
            queryset = queryset.filter(card_status=status.lower())
        if card_number:
            queryset = queryset.filter(card_number__icontains=card_number)
        if phone:
            queryset = queryset.filter(phone_number__icontains=phone)

        total = queryset.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("❌ No cards found for given filters"))
            return

        with open(full_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Card Number', 'Expire', 'Phone Number', 'Card Status', 'Balance', 'Created At'])

            for card in queryset:
                writer.writerow([
                    card.card_number,
                    card.expire,
                    card.phone_number,
                    card.card_status,
                    card.balance,
                    card.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                ])

        self.stdout.write(self.style.SUCCESS(f"✅ Exported {total} cards to {full_path}"))

