from pyhomebroker import HomeBroker
import time


broker = 265
dni = '26386662'
user = 'piolifl'
password = 'd3x87bXYh4#5m!E'
account_id = '10214'

hb = HomeBroker(int(broker))

hb.auth.login(dni=dni, user=user, password=password, raise_exception=True)

hb.online.connect()

hb.online.subscribe_securities('government_bonds', 'spot')

orders = hb.orders.get_orders_status(account_id)

hb.online.subscribe_order_book('AL30', 'spot')

hb.online.unsubscribe_securities('government_bonds', 'spot')

hb.online.disconnect()


## Send a buy order to the market
#symbol = input('Simbolo: ')
#settlement = input('Vencimiento: ')
#price = input('Precio: ')
#size = input('Cantidad: ')
#order_number = hb.orders.send_buy_order(symbol, settlement, float(price), int(size))
#print(order_number)

## Send a sell order to the market
#symbol = input('Simbolo: ')
#settlement = input('Vencimiento: ')
#price = input('Precio: ')
#size = input('Cantidad: ')
#order_number = hb.orders.send_sell_order(symbol, settlement, float(price), int(size))
#print(order_number)

## Cancel an order
#order_number = input('Order number: ')
#hb.orders.cancel_order(account_id, order_number)

## Cancel all the orders
#hb.orders.cancel_all_orders(account_id)

'''
symbol  settlement  operation_type      size    price   remaining_size      datetime             status    cancellable   order_number
AL30    spot        BUY                 1       6490    1                   2022-08-01 10:47:55  OFFERED   True          1744884     
'''