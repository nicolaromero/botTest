import requests
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

# Calcular la diferencia entre "limit" y "precio"
diferencia = float(limit) - float(precio)

# Calcular el porcentaje de diferencia entre "limit" y "precio"
porcentaje_diferencia = (diferencia / float(precio)) * 100

# Imprimir el resultado
print(
    f"El valor de 'limit' es {porcentaje_diferencia:.2f}% diferente del precio de punta.")

if float(limit) > float(precio):
    print("El valor de 'limit' es mayor que el precio de punta.")
else:
    print("El valor de 'limit' es menor o igual que el precio de punta.")
