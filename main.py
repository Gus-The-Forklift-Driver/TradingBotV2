from utils import *
from marketData import btcEur
from ui import ui
from backend import backendTest
import strategy
from secret import ReadOnly
from binance.client import Client

client = Client(ReadOnly['Api Key'], ReadOnly['Secret Key'])

# get and create the market data
btcEur = client.get_klines(symbol='BTCEUR', interval='15m', limit=1000)
BTCEUR = marketData(btcEur)

# parameters of the strategy
parameters = {"consecutiveGreen": 2, "consecutiveRed": 3,
              "BuyMultiplier": 100, 'SellMultiplier': 25}

# assign the strategy
test1 = strategy.buyTheRed(parameters)

# create the backend strategy
backend = backendTest(BTCEUR, test1)

# run the initial test
results = backend.runTest()

# when a setting is changed update the backend test automaticaly


def update(sender, app_data, user_data):
    parameters[sender] = int(app_data)
    backend.updateParameters(parameters)
    results = backend.runTest()
    viz.updateTest(BTCEUR, results)


# create and show main ui
viz = ui()
viz.create_main_ui(BTCEUR, test1, update, results)
viz.show_ui()
