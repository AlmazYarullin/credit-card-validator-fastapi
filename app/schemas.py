from pydantic import BaseModel


class CardOut(BaseModel):
    brand: str = ''
    bank: str = ''
    error_code: str
