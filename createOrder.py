import requests
from config import auth

# MercadoTest
market_id = 'btc-ars'

url = f'https://www.buda.com/api/v2/markets/{market_id}/orders'
response = requests.post(url, auth=auth, json={
    'type': 'Bid',
    'price_type': 'limit',
    'limit': [PRECIO],
    'amount': [MONTO],
})
print(response.json())
