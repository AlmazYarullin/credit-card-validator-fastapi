from sqlalchemy import func

from .models import Card
from .schemas import CardOut


def check_card_number(card_number: str, db) -> CardOut:
    number_len = len(card_number)
    is_full_number = False

    if number_len < 6:
        return CardOut(error_code=1)

    if number_len < 16:
        card_number += '0' * (16 - number_len)
    elif number_len == 16:
        is_full_number = True
    else:
        return CardOut(error_code=4)

    if is_full_number:
        card = db.query(Card).where(Card.range_start <= card_number).where(card_number <= Card.range_end).first()
        if card:
            return CardOut(error_code=0, bank=card.issuer_name, brand=card.brand)

    card_bin = int(card_number[:6])
    card = db.query(Card).filter(func.div(Card.range_start, 10 ** 10) == card_bin).first()
    if card:
        return CardOut(error_code=3 if is_full_number else 2, bank=card.issuer_name, brand=card.brand)
    else:
        return CardOut(error_code=3 if is_full_number else 2)
