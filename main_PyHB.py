# Carga de librerias necesarias:

import time
from pyhomebroker import HomeBroker
import xlwings as xw
import Options_Helper_HM
import pandas as pd
import config

# Lista de los activos que va a levantar:

ACC = Options_Helper_HM.getAccionesList()
cedears = Options_Helper_HM.getCedearsList()
cauciones = Options_Helper_HM.cauciones
options = Options_Helper_HM.getOptionsList()
bonos = Options_Helper_HM.getBonosList()
letras = Options_Helper_HM.getLetrasList()
#ONS = Options_Helper_HM.getONSList()
#PanelGeneral = Options_Helper_HM.getPanelGeneralList()
options = options.rename(columns={"bid_size": "bidsize", "ask_size": "asksize"})
everything = ACC.append(bonos)
everything = everything.append(letras)
#everything = everything.append(PanelGeneral)
#everything = everything.append(ONS)
everything = everything.append(cedears)

listLength = len(everything) + 2

wb = xw.Book('EPGBliteHB.xlsx')
shtTest = wb.sheets('HomeBroker')
shtTickers = wb.sheets('Tickers')

print("OK: ACTUALIZANDO INFORMACION")

def on_options(online, quotes):
    global options
    thisData = quotes
    thisData = thisData.drop(['expiration', 'strike', 'kind'], axis=1)
    thisData['change'] = thisData["change"] / 100
    thisData['datetime'] = pd.to_datetime(thisData['datetime'])
    thisData = thisData.rename(columns={"bid_size": "bidsize", "ask_size": "asksize"})
    options.update(thisData)

def on_securities(online, quotes):
    global ACC

    print(quotes)
    thisData = quotes
    thisData = thisData.reset_index()
    thisData['symbol'] = thisData['symbol'] + ' - ' +  thisData['settlement']
    thisData = thisData.drop(["settlement"], axis=1)
    thisData = thisData.set_index("symbol")
    thisData['change'] = thisData["change"] / 100
    thisData['datetime'] = pd.to_datetime(thisData['datetime'])
    everything.update(thisData)

def on_repos(online, quotes):
    global cauciones
    thisData = quotes
    thisData = thisData.reset_index()
    thisData = thisData.set_index("symbol")
    thisData = thisData[['PESOS' in s for s in quotes.index]]
    thisData = thisData.reset_index()
    thisData['settlement'] = pd.to_datetime(thisData['settlement'])
    thisData = thisData.set_index("settlement")
    thisData['last'] = thisData["last"] / 100
    thisData['bid_rate'] = thisData["bid_rate"] / 100
    thisData['ask_rate'] = thisData["ask_rate"] / 100
    thisData = thisData.drop(['open', 'high', 'low', 'volume', 'operations', 'datetime'], axis=1)
    thisData = thisData[['last', 'turnover', 'bid_amount', 'bid_rate', 'ask_rate', 'ask_amount']]
    cauciones.update(thisData)


def on_error(online, error):
    print("Error Message Received: {0}".format(error))

hb = HomeBroker(int(config.broker),
                on_options=on_options,
                on_securities=on_securities,
                on_repos=on_repos,
                on_error=on_error)

hb.auth.login(dni=config.dni,
              user=config.user,
              password=config.password,
              raise_exception=True)

hb.online.connect()
hb.online.subscribe_options()
hb.online.subscribe_securities('bluechips', '48hs')                       # Acciones del Panel lider - 48hs
hb.online.subscribe_securities('bluechips', '24hs')                       # Acciones del Panel lider - 24hs
hb.online.subscribe_securities('bluechips', 'SPOT')                       # Acciones del Panel lider - Contado Inmediato
hb.online.subscribe_securities('government_bonds', '48hs')                # Bonos - 48hs
hb.online.subscribe_securities('government_bonds', '24hs')                # Bonos - 24hs
hb.online.subscribe_securities('government_bonds', 'SPOT')                # Bonos - Contado Inmediato
hb.online.subscribe_securities('cedears', '48hs')                       # CEDEARS - 48hs
hb.online.subscribe_securities('cedears', '24hs')                       # CEDEARS - 24hs
hb.online.subscribe_securities('cedears', 'SPOT')                       # CEDEARS - Contado Inmediato
# hb.online.subscribe_securities('general_board', '48hs')                 # Acciones del Panel general - 48hs
# hb.online.subscribe_securities('general_board', '24hs')                 # Acciones del Panel general - 24hs
# hb.online.subscribe_securities('general_board', 'SPOT')                 # Acciones del Panel general - Contado Inmediato
hb.online.subscribe_securities('short_term_government_bonds', '48hs')     # LETRAS - 48hs
hb.online.subscribe_securities('short_term_government_bonds', '24hs')   # LETRAS - 24hs
hb.online.subscribe_securities('short_term_government_bonds', 'SPOT')   # LETRAS - Contado Inmediato
# hb.online.subscribe_securities('corporate_bonds', '48hs')                 # Obligaciones Negociables - 48hs
# hb.online.subscribe_securities('corporate_bonds', '24hs')               # Obligaciones Negociables - 24hs
# hb.online.subscribe_securities('corporate_bonds', 'SPOT')               # Obligaciones Negociables - Contado Inmediato
hb.online.subscribe_repos()

''' Referencias:
bluechips = Acciones del Panel Lider
goverment_bonds = Bonos
general_board = Acciones del Panel General
short_term_government_bonds = Letras
corporate_bonds = Obligaciones Negociables'''

while True:
    '''try:
        oRange = 'A' + str(listLength)
        shtTest.range('A1').options(index=True, header=True).value = everything
        shtTest.range(oRange).options(index=True, header=False).value = options
        shtTest.range('S2').options(index=True, header=False).value = cauciones
        time.sleep(2)
    except:
        print('Hubo un error al actualizar excel')'''

    sht = wb.sheets['HomeBroker']
    al30 = sht.range('A11:F11').value
    ran = sht.range('A11:F13').options(pd.DataFrame).value
    ra2 = sht.range('A11').expand().options(pd.DataFrame).value
    #wb.save('EPGBliteHB.xlsx')
    #app = xw.apps.active
    #app.quit()
    #print(sht.range('A11').expand('right').value)
    print(al30[5],ra2)
