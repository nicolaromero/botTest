import time
import requests
from datetime import datetime
from config import auth

i = 0  # Inicializar la variable que cuenta las ejecuciones

while True:
    # MercadoTest
    market_id = 'btc-ars'
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")

    # Obtener mis ordenes
    urlOrders = f'https://www.buda.com/api/v2/markets/{market_id}/orders'
    responseOrders = requests.get(urlOrders, auth=auth, params={
        'state': 'pending',
        'per': 20,
        'page': 1,
    })
    print(f"Init {i} - {date}")
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
    print("Precio punta:", precio)
    print("Cantidad punta:", cantidad)

    limit = responseOrders.json()['orders'][0]['limit'][0]

    # Calcular el porcentaje de diferencia entre "limit" y "precio"
    price_dif = ((float(limit) - float(precio)) / float(precio)) * 100
    print(
        f"El valor de 'limit' es {price_dif:.2f}% diferente del precio de punta.")

    # Check dif precio
    if price_dif < -10:
        order_id = responseOrders.json()['orders'][0]['id']
        url_cancel = f'https://www.buda.com/api/v2/orders/{order_id}'
        response_cancel = requests.put(url_cancel, auth=auth, json={
            'state': 'canceling',
        })
        print("Orden cancelada < -10%: ")
        print(response_cancel.json())

        # Calcular nuevo precio
        new_price = float(precio) * (1 - 0.094)

        url_balance = f'https://www.buda.com/api/v2/balances'
        response_balance = requests.get(url_balance, auth=auth)
        print("Total balance: ")
        print(response_balance.json())

        #new_amount = float(response_balance.json()['balances']['amount'][0])

        # Iterate over "balances" array to find the desired object
        time.sleep(1)
        for balance in response_balance.json()['balances']:
            if balance['id'] == 'ARS':
                balanceARS = float(balance['available_amount'][0])
                new_amount = (balanceARS-1)/new_price
                print("Balance: ", balanceARS)
                print("Nuevo monto: ", new_amount)
                break

        time.sleep(1)
        url_newOrder = f'https://www.buda.com/api/v2/markets/{market_id}/orders'
        response_newOrder = requests.post(url_newOrder, auth=auth, json={
            'type': 'Bid',
            'price_type': 'limit',
            'limit': new_price,
            'amount': new_amount,
        })
        print("NewOrder:")
        print(response_newOrder.json())

    # Incrementar la variable que cuenta las ejecuciones
    i += 1

    # Verificar si se ha alcanzado el número máximo de ejecuciones
    if i >= 180:
        print(f"END - Ejecución {i}")
        break

    # Agrega un retraso en segundos antes de la siguiente ejecución
    time.sleep(300)
