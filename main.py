from utils import *
from marketData import btcEur
from ui import ui
from backend import backendTest
import strategy
from secret import ReadAndWrite
from binance.client import Client
import dearpygui.dearpygui as dpg

client = Client(ReadAndWrite['Api Key'], ReadAndWrite['Secret Key'])

# get and create the market data
#btcEur = client.get_klines(symbol='BTCEUR', interval='15m', limit=200)
#ethEur = client.get_klines(symbol='ETHEUR', interval='15m', limit=200)
btcEur = client.get_historical_klines(
    'BTCEUR', '15m', "15 Nov, 2021", "19 Nov, 2021")

global Market
Market = marketData(btcEur)


# parameters of the strategy
parameters = {"consecutiveGreen": 2, "consecutiveRed": 3,
              "BuyMultiplier": 100, 'SellMultiplier': 25}

#parameters = {}

# assign the strategy
test1 = strategy.buyTheRed(parameters)

# create the backend strategy
backend = backendTest(test1)

# run the initial test
results = backend.runTest(Market)

# when a setting is changed update the backend test automaticaly


def update(sender, app_data, user_data):
    if sender == 'simulation_update_button':
        results = backend.runTest(Market)
        viz.updateTest(Market, results)
    else:
        parameters[sender] = int(app_data)
        backend.updateParameters(parameters)
        results = backend.runTest(Market)
        viz.updateTest(Market, results)


def update_market_data(sender, app_data):
    FIAT = dpg.get_value('FIAT currency')
    CRYPTO = dpg.get_value('CRYPTO currency')
    start = dpg.get_value('market_start')
    end = dpg.get_value('maket_end')
    interval = dpg.get_value('time_interval')
    global Market
    if dpg.get_value('use_current_time'):
        try:
            data = client.get_klines(
                symbol=CRYPTO+FIAT, interval=interval, limit=200)
        except:
            print('failed to fetch market data')
        else:
            Market = marketData(data)
    else:
        try:
            data = client.get_historical_klines(
                CRYPTO+FIAT, interval, start, end)
        except:
            print('failed to fetch market data')
        else:
            Market = marketData(data)


# create and show main ui
viz = ui()
viz.create_main_ui(Market, test1, update, update_market_data, results)
viz.show_ui()
