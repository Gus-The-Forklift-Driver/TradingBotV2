from utils import *
from marketData import btcEur
from ui import ui
from backend import backendTest
import strategy
from secret import ReadAndWrite
from binance.client import Client

client = Client(ReadAndWrite['Api Key'], ReadAndWrite['Secret Key'])

# get and create the market data
#btcEur = client.get_klines(symbol='BTCEUR', interval='15m', limit=200)
#ethEur = client.get_klines(symbol='ETHEUR', interval='15m', limit=200)
btcEur = client.get_historical_klines(
    'BTCEUR', '15m', "15 Nov, 2021", "19 Nov, 2021")
ethEur = client.get_historical_klines(
    'ETHEUR', '15m', "15 Nov, 2021", "19 Nov, 2021")
BTCEUR = marketData(btcEur)
ETHEUR = marketData(ethEur)

# parameters of the strategy
parameters = {"consecutiveGreen": 2, "consecutiveRed": 3,
              "BuyMultiplier": 100, 'SellMultiplier': 25, 'BTCdata': BTCEUR}

#parameters = {}

# assign the strategy
test1 = strategy.buyTheRed(parameters)

# create the backend strategy
backend = backendTest(test1)

# run the initial test
results = backend.runTest(ETHEUR)

# when a setting is changed update the backend test automaticaly


def update(sender, app_data, user_data):
    parameters[sender] = int(app_data)
    backend.updateParameters(parameters)
    results = backend.runTest(ETHEUR)
    viz.updateTest(ETHEUR, results)


# create and show main ui
viz = ui()
viz.create_main_ui(ETHEUR, test1, update, results)
viz.show_ui()
