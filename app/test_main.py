import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Card
from .main import app, get_db
from .settings import settings

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = settings.get_db_connection_string() + '_test'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

test_data = {
    'range_start': 1234565000000000,
    'range_end': 1234565999999999,
    'issuer_country': 'RUS',
    'issuer_name': 'tinkoff',
    'brand': 'Visa',
    'product_code': 'F',
    'product_name': 'Visa Classic',
    'card_type': 'Debit'
}


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def setup_db():
    db = next(override_get_db())
    card = Card(**test_data)
    db.add(card)
    db.commit()

    yield

    db.delete(card)
    db.commit()
    next(override_get_db())


def check_number(number: str, expected_answer: dict):
    response = client.get(f"/{number}")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == expected_answer


def test_number_full_correct(setup_db):
    check_number("1234565111111111", {"brand": "Visa", "bank": "tinkoff", "error_code": "0"})


def test_number_full_incorrect(setup_db):
    check_number("1234569111111111", {"brand": "Visa", "bank": "tinkoff", "error_code": "3"})


def test_number_less_than_six(setup_db):
    check_number("123", {"brand": "", "bank": "", "error_code": "1"})


def test_number_not_full(setup_db):
    check_number("123456", {"brand": "Visa", "bank": "tinkoff", "error_code": "2"})
    check_number("1234560000000", {"brand": "Visa", "bank": "tinkoff", "error_code": "2"})
    check_number("1234569000000", {"brand": "Visa", "bank": "tinkoff", "error_code": "2"})
    check_number("1134569000000", {"brand": "", "bank": "", "error_code": "2"})


def test_number_more_than_16(setup_db):
    check_number("1" * 17, {"brand": "", "bank": "", "error_code": "4"})
