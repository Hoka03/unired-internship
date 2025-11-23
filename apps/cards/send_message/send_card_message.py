import requests, os

from config.settings import TELEGRAM_BOT_TOKEN


def send_card_to_message(card):
    message = (
        f"💳 *Card Info:*\n"
        f"• Card number: `{card.card_number}`\n"
        f"• Phone: `{card.phone_number}`\n"
        f"• Balance: `{card.balance}`\n"
        f"• Expire: `{card.expire}`\n"
        f"• Status: `{card.card_status}`"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": os.environ.get("TELEGRAM_CHAT_ID"),
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except:
        return False
