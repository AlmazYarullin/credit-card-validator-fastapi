from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal
from .schemas import CardOut
from .utils import check_card_number

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/{card_number}', response_model=CardOut)
async def check_card(card_number: str, db: Session = Depends(get_db)):
    return check_card_number(card_number, db)
