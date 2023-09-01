import requests
import time
from config import auth

# MercadoTest
market_id = 'btc-clp'
while True:
# Obtener precio de punta en las órdenes de tipo "Bid"
    urlBook = f'https://www.buda.com/api/v2/markets/{market_id}/order_book'
    responseBook = requests.get(urlBook)
    responseBook_json = responseBook.json()
    bids = responseBook_json['order_book']['bids']
    precio_punta_compra = float(bids[0][0])
    print("Precio punta compra:", precio_punta_compra)

# Obtener precio de punta en las órdenes de tipo "Ask"
    asks = responseBook_json['order_book']['asks']
    precio_punta_venta = float(asks[0][0])
    print("Precio punta venta:", precio_punta_venta)

    spread = precio_punta_venta - precio_punta_compra
    print ("Spread:", spread)

# Obtener mis órdenes pendientes
    urlOrders = f'https://www.buda.com/api/v2/markets/{market_id}/orders'
    responseOrders = requests.get(urlOrders, auth=auth, params={
        'state': 'pending',
        'per': 20,
        'page': 1,
    })
    orders = responseOrders.json()['orders']
    if not orders:
        print("No hay órdenes pendientes.")
        
        # Calcular el nuevo precio
        new_price = precio_punta_venta - 1
        max_price = precio_punta_compra + (spread / 2)
        print("Nuevo precio: ", new_price)
        print("Maximo precio: ", max_price)
        
        # Iterar sobre el array "balances" para encontrar el objeto deseado
        url_balance = f'https://www.buda.com/api/v2/balances'
        response_balance = requests.get(url_balance, auth=auth)
        print(response_balance.json())

        # Iterar sobre el array "balances" para encontrar el objeto deseado
        time.sleep(1)
        desired_currency = 'BTC'
        for balance in response_balance.json()['balances']:
            if balance['id'] == desired_currency:
                balanceBTC = float(balance['available_amount'][0])
                new_amount = (balanceBTC)
                print("Balance BTC:", balanceBTC)
                print("Nuevo monto:", new_amount)
                break

        # Crear una nueva orden de compra
        url_newOrder = f'https://www.buda.com/api/v2/markets/{market_id}/orders'
        response_newOrder = requests.post(url_newOrder, auth=auth, json={
            'type': 'Ask',
            'price_type': 'limit',
            'limit': new_price,
            'amount': new_amount,
            'force': True
        })
        print("Nueva orden de venta:", response_newOrder.json())
    else:
        first_order = orders[0]
        order_id = first_order['id']
        limit = float(first_order['limit'][0])
        print("Limit:", limit)
    
        if limit  > precio_punta_venta:
            # Guardar valores de monto y precio antes de cancelar la orden
            original_amount = float(first_order['amount'][0])
            original_price = float(first_order['limit'][0])

            # Cancelar la orden pendiente
            url_cancel = f'https://www.buda.com/api/v2/orders/{order_id}'
            response_cancel = requests.put(url_cancel, auth=auth, json={
                'state': 'canceling',
            })
            print("Orden cancelada:", response_cancel.json())

            # Calcular el nuevo precio
            new_price = precio_punta_venta - 1
            max_price = precio_punta_compra + (spread / 2)
            print("Nuevo precio: ", new_price)
            print("Maximo precio: ", max_price)
            
            if new_price >= max_price:
                # Iterar sobre el array "balances" para encontrar el objeto deseado
                url_balance = f'https://www.buda.com/api/v2/balances'
                response_balance = requests.get(url_balance, auth=auth)
                print(response_balance.json())

                # Iterar sobre el array "balances" para encontrar el objeto deseado
                time.sleep(1)
                desired_currency = 'BTC'
                for balance in response_balance.json()['balances']:
                    if balance['id'] == desired_currency:
                        balanceBTC = float(balance['available_amount'][0])
                        new_amount = (balanceBTC)
                        print("Balance BTC:", balanceBTC)
                        print("Nuevo monto:", new_amount)
                        break

                # Crear una nueva orden de compra
                url_newOrder = f'https://www.buda.com/api/v2/markets/{market_id}/orders'
                response_newOrder = requests.post(url_newOrder, auth=auth, json={
                    'type': 'Ask',
                    'price_type': 'limit',
                    'limit': new_price,
                    'amount': new_amount,
                    'force': True
                })
                print("Nueva orden de venta:", response_newOrder.json())
            else:
                # Si no se cumplen las condiciones, crear una nueva orden con los valores originales
                url_newOrder = f'https://www.buda.com/api/v2/markets/{market_id}/orders'
                response_newOrder = requests.post(url_newOrder, auth=auth, json={
                    'type': 'Ask',
                    'price_type': 'limit',
                    'limit': original_price,
                    'amount': original_amount,
                })
                print("Nueva orden de compra con valores originales:", response_newOrder.json())
        else:
            print("La orden pendiente se mantiene. ¡Estás de puntero!")
    time.sleep(2)