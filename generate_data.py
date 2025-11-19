import random
from openpyxl import Workbook


def luhn_generate(prefix: str, length: int) -> str:
    """
        Generate a valid card number using the Luhn algorithm.

        Args:
            prefix (str): Starting digits of the card number (e.g., "8600").
            length (int): Total desired length of the card number (commonly 16).

        Returns:
            str: A complete card number that passes the Luhn check.

        Example:
            >>> luhn_generate("8600", 16)
            "8600123456789012"
    """
    number = prefix
    while len(number) < (length - 1):
        number += str(random.randint(0, 9))

    digits = [int(x) for x in number]
    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9

    checksum = (10 - (sum(digits) % 10)) % 10
    return number + str(checksum)


def generate_cards_excel(filename: str = "cards.xlsx", rows: int = 500):
    """
        Generate an Excel file with randomly generated card data.

        Each row contains:
            - card_number (Luhn-valid)
            - expire (random expiry date in multiple formats)
            - phone (random phone number in multiple formats)
            - status (active, inactive, expired)
            - balance (random float up to 1.2 billion)

        Args:
            filename (str, optional): Output Excel file name. Defaults to "cards.xlsx".
            rows (int, optional): Number of card records to generate. Defaults to 500.

        Returns:
            None: Saves an Excel file to disk.

        Example:
            >>> generate_cards_excel("test_cards.xlsx", 10)
            # Creates "test_cards.xlsx" with 10 rows of card data.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Cards"

    columns = ["card_number", "expire", "phone", "status", "balance"]
    ws.append(columns)

    statuses = ["active", "inactive", "expired"]
    card_prefixes = ["8600", "5614", "4916"]

    for _ in range(rows):
        prefix = random.choice(card_prefixes)
        card_number = luhn_generate(prefix, 16)

        # Random expiry formats
        expire_formats = [
            "{:02d}/{:04d}",
            "{:04d}-{:02d}",
            "{:02d}.{:04d}",
            "{:02d}-{:04d}",
            "{:04d}",
            "{:02d}",
        ]
        fmt = random.choice(expire_formats)
        if fmt == "{:04d}":
            expire = fmt.format(random.randint(2020, 2050))
        elif fmt == "{:02d}":
            expire = fmt.format(random.randint(1, 12))
        elif fmt in ["{:04d}-{:02d}"]:
            expire = fmt.format(random.randint(2020, 2030), random.randint(1, 12))
        else:
            expire = fmt.format(random.randint(1, 12), random.randint(2020, 2030))

        # Random phone formats
        phone_formats = [
            "+998{:02d}{:03d}{:02d}{:2d}",
            "{:02d}{:03d}{:02d}{:02d}",
            "99 {:03d} {:02d} {:02d}",
            ""
        ]
        fmt_phone = random.choice(phone_formats)
        if fmt_phone == "99 {:03d} {:02d} {:02d}":
            phone = fmt_phone.format(
                random.randint(100, 999),
                random.randint(10, 99),
                random.randint(10, 99)
            )
        elif fmt_phone == '':
            phone = ''
        else:
            phone = fmt_phone.format(
                random.randint(10, 99),
                random.randint(100, 999),
                random.randint(10, 99),
                random.randint(10, 99)
            )

        status = random.choice(statuses)
        balance = round(random.uniform(0, 1_200_000_000), 2)

        ws.append([card_number, expire, phone, status, balance])

    wb.save(filename)
    print(f"{rows} cards have been generated into {filename}")

generate_cards_excel("cards.xlsx", 50)
