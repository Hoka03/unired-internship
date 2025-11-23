from django.contrib import admin, messages

from apps.cards.send_message.send_card_message import send_card_to_message


@admin.action(description="Send selected cards to Telegram")
def send_selected_cards_to_telegram(self, request, queryset):
    success = 0
    fail = 0
    for card in queryset:
        if send_card_to_message(card):
            success += 1
        else:
            fail += 1

    self.message_user(
        request,
        f"{success} ta karta Telegramga yuborildi, {fail} ta karta yuborilmadi.",
        messages.SUCCESS if fail == 0 else messages.WARNING
    )
