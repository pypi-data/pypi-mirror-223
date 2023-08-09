import random
from urllib.parse import urlencode, quote
from pywallex.schemas import PaymentModel
from pywallex.utils import calculate_sign


class Widget:
    PaymentModel = PaymentModel

    def __init__(self, merchant_id, secret_key, base_url: str = 'https://wallex.online/widget/%d?data=%s'):
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.base_url = base_url

    def create_payment(self, data: PaymentModel):
        data = {
            **data.model_dump(),
            **{
                'price': int(data.price * 100),
                'uuid': random.randint(10000, 99999) if data.uuid is None else data.uuid
            }
        }

        data['sign'] = calculate_sign(self.secret_key, data)
        data = urlencode(data, quote_via=quote)

        return self.BASE_URL % (self.merchant_id, data)
