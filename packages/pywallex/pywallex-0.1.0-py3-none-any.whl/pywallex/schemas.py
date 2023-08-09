from pydantic import BaseModel


class FiatPayModel(BaseModel):
    amount: float
    currency: str
    bank: str
    number: str
    month: int
    year: int
    fiat: str
    cardholder: str
    date_of_birth: str
    type: str = 'fiat'


class CryptoPayModel(BaseModel):
    address: str
    amount: float
    currency: str
    type: str = 'crypto'


class PaymentModel(BaseModel):
    client: str
    product: str
    price: float
    quantity: int
    message: str
    description: str
    currency: str = 'USDT'
    fiat_currency: str = 'rub'
    language: str = 'ru'
    uuid: str | None = None
