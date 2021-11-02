from utils import *
from marketData import btcEur
from ui import ui
from backend import backendTest
import strategy

# create the market data
BTCEUR = marketData(btcEur)

# parameters of the strategy
parameters = {"consecutiveGreen": 1, "consecutiveRed": 2, "multiplier": 5}

# assign the strategy
test1 = strategy.buyTheRed(parameters)

# create the backend strategy
backend = backendTest(BTCEUR, test1)

# run the initial test
results = backend.runTest()

# when a setting is changed update the backend test automaticaly


def update(sender, app_data, user_data):
    print(sender)
    print(app_data)
    parameters[sender] = int(app_data)
    backend.updateParameters(parameters)
    results = backend.runTest()
    viz.updateTest(BTCEUR, results)


# create and show main ui
viz = ui()
viz.create_main_ui(BTCEUR, test1, update, results)
viz.show_ui()
