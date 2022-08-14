from pyhomebroker import HomeBroker

broker = 265
dni = '26386662'
user = 'piolifl'
password = 'd3x87bXYh4#5m!E'

hb = HomeBroker(int(broker))

snapshot = hb.online.get_market_snapshot()

print(snapshot)

    
