# Credit card validator API

## Description
This is a simple API that allows you to check if a credit card number is correct

## Installation and Launch

Clone the repo:
```shell
git clone https://github.com/AlmazYarullin/credit-card-validator-fastapi.git
```

### 1. Using docker

```shell
docker-compose up -d
```

### 2. Without docker
Comple these steps in root folder


1. Install requirements:
```shell
pip install -r requirements.txt
```
2. Apply migrations:
```shell
alembic upgrade --head
```

3. Setup environment. Example:
```shell
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_SERVER=localhost
export POSTGRES_DB=postgres
```

4. Launch the application:
```shell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Introduction

You can check Swagger UI after launching the app at this address: http://localhost:8000/docs

### Responses
```json
{
  "brand": "string",
  "bank": "string",
  "error_code": "string"
}
```
The `brand` attribute contains an information about card brand "Visa" or "Mastercard".<br>
The `bank` attribute contains an information about which bank the card belongs to.<br>
The `error_code` attribute describes an error code.<br>

### Error codes
| Error code | Meaning                                |
|:----------:|----------------------------------------|
|     0      | Card number is correct                 |
|     1      | Card number is too short (less than 6) |
|     2      | Card number is not full (less than 16) |
|     3      | Card number is full and incorrect      |
|     4      | Card number is too long (more than 16) |

