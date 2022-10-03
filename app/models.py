from sqlalchemy import Column, String, Numeric

from .database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Numeric(scale=19), primary_key=True)
    range_start = Column(Numeric(scale=19), unique=True, index=True, nullable=False)
    range_end = Column(Numeric(scale=19), unique=True, index=True, nullable=False)
    issuer_country = Column(String)
    issuer_name = Column(String)
    brand = Column(String)
    product_code = Column(String)
    product_name = Column(String)
    card_type = Column(String)
