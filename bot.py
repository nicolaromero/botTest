import requests
import time
from config import auth

# MercadoTest
market_id = 'btc-ars'

#url = f'https://www.buda.com/api/v2/me'
#response = requests.get(url, auth=auth)

#market_id = 'btc-ars'
#url = f'https://www.buda.com/api/v2/markets/{market_id}/orders'
# response = requests.post(url, auth=auth, json={
#    'type': 'Bid',
#    'price_type': 'limit',
#    'limit': 9000000,
#    'amount': 0.00002500,
# })
# print(response.json())

# Obtener mis ordenes
urlOrders = f'https://www.buda.com/api/v2/markets/{market_id}/orders'
responseOrders = requests.get(urlOrders, auth=auth, params={
    'state': 'pending',
    'per': 20,
    'page': 1,
})
print(responseOrders.json())


# Obtener precio de punta en el libro
urlBook = f'https://www.buda.com/api/v2/markets/{market_id}/order_book'
responseBook = requests.get(urlBook)
responseBook_json = responseBook.json()
bids = responseBook_json['order_book']['bids']
# El primer elemento en la lista de bids es la punta
primera_punta = bids[0]
precio = primera_punta[0]
cantidad = primera_punta[1]
print("Precio:", precio)
print("Cantidad:", cantidad)

limit = responseOrders.json()['orders'][0]['limit'][0]

# Calcular el porcentaje de diferencia entre "limit" y "precio"
price_dif = ((float(limit) - float(precio)) / float(precio)) * 100

# nuevo precio
new_price = float(precio) * (1 - 0.1)

# check precio
if price_dif < -10:
    order_id = responseOrders.json()['orders'][0]['id']
    url_cancel = f'https://www.buda.com/api/v2/orders/{order_id}'
    response_cancel = requests.put(url_cancel, auth=auth, json={
        'state': 'canceling',
    })
    print(response_cancel.json())

    new_price = float(precio) * (1 - 0.1)

    url_balance = f'https://www.buda.com/api/v2/balances'
    response_balance = requests.get(url_balance, auth=auth)
    print(response_balance.json())

    #new_amount = float(response_balance.json()['balances']['amount'][0])

    # Iterate over the "balances" array to find the desired object
    time.sleep(1)
    for balance in response_balance.json()['balances']:
        if balance['id'] == 'ARS':
            balanceARS = float(balance['available_amount'][0])
            new_amount = (balanceARS-1)/new_price
            print(balanceARS)
            print(new_amount)
            break

    time.sleep(1)
    url_newOrder = f'https://www.buda.com/api/v2/markets/{market_id}/orders'
    response_newOrder = requests.post(url_newOrder, auth=auth, json={
        'type': 'Bid',
        'price_type': 'limit',
        'limit': new_price,
        'amount': new_amount,
    })
    print(response_newOrder.json())


####### TEST#########
# Imprimir el resultado
print(new_price)
print(
    f"El valor de 'limit' es {price_dif:.2f}% diferente del precio de punta.")

if float(limit) > float(precio):
    print("El valor de 'limit' es mayor que el precio de punta.")
else:
    print("El valor de 'limit' es menor o igual que el precio de punta.")
