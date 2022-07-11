from utils import *


class CoingeckoApi():
    def __init__(self) -> None:
        from pycoingecko import CoinGeckoAPI
        self.cg = CoinGeckoAPI()

    def getMarket_Data(self):
        return marketData(self.cg.get_coin_ohlc_by_id('bitcoin', 'eur', 1))


class BinanceApi():
    def __init__(self) -> None:
        from secret import ReadAndWrite
        from binance.client import Client
        self.client = Client(
            ReadAndWrite['Api Key'], ReadAndWrite['Secret Key'])

    def getMarket_Data(self):
        # get and create the market data
        #btcEur = client.get_klines(symbol='BTCEUR', interval='15m', limit=200)
        #ethEur = client.get_klines(symbol='ETHEUR', interval='15m', limit=200)
        btcEur = self.client.get_historical_klines(
            'BTCEUR', '15m', "15 Nov, 2021", "19 Nov, 2021")
        return marketData(btcEur)
