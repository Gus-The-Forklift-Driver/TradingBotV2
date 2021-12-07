import paper
from utils import marketData


class backendTest():
    def __init__(self, strategy):
        self.wallet = paper.wallet()
        self.strategy = strategy

    # run the simulation for a strategy according to given parameters
    def runTest(self, marketData):
        self.wallet.balanceEUR = 500
        self.wallet.balanceBTC = 0
        testResults = {'BuyOperations': 0,
                       'SellOperations': 0,
                       'CumulatedGains': 0,
                       'TotalGains': 0,
                       'Fees': 0,
                       'EurOverTime': [],
                       'BtcOverTime': [],
                       'BalanceOverTime': [],
                       'BotPerformance': [],
                       'buysNsells': [],
                       'CumulativeBotPerformance': 0,
                       'CumulativeBtcPerformance': 0
                       }
        BuynSell = self.strategy.populate_buy_sell(marketData)

        testResults['buysNsells'] = [0]*marketData.lenght
        # iterate through the market data
        previousBalance = self.wallet.balanceEUR
        previousPerformance = 0
        for candle in range(marketData.lenght):
            price = marketData.close[candle]
            if BuynSell[candle] > 0 and self.wallet.balanceEUR > 0:
                amount = self.wallet.balanceEUR*BuynSell[candle]
                try:
                    fees = self.wallet.buyMarket(price, amount)
                except ValueError:
                    try:
                        fees = self.wallet.buyMarket(price)
                    except ValueError:
                        pass
                    else:
                        testResults['Fees'] += fees
                        testResults['BuyOperations'] += 1
                        testResults['buysNsells'][candle] = amount
                else:
                    testResults['Fees'] += fees
                    testResults['BuyOperations'] += 1
                    testResults['buysNsells'][candle] = amount

            elif BuynSell[candle] < 0 and self.wallet.balanceBTC > 0:
                amount = self.wallet.balanceBTC*BuynSell[candle]*-1
                try:
                    fees = self.wallet.sellMarket(price, amount)
                except ValueError:
                    try:
                        fees = self.wallet.sellMarket(price)
                    except ValueError:
                        pass
                    else:
                        testResults['Fees'] += fees
                        testResults['SellOperations'] += 1
                        testResults['buysNsells'][candle] = -amount * price
                else:
                    testResults['Fees'] += fees
                    testResults['SellOperations'] += 1
                    testResults['buysNsells'][candle] = -amount * price
            # logs current progress
            testResults['EurOverTime'].append(self.wallet.balanceEUR)
            testResults['BtcOverTime'].append(self.wallet.balanceBTC)
            testResults['BalanceOverTime'].append(
                self.wallet.balanceEUR+self.wallet.balanceBTC*price)
            # calculates percent profitable
            BtcPerformance = (
                (marketData.close[candle] - marketData.open[candle])/marketData.open[candle])*100
            BotPerformance = ((testResults['BalanceOverTime'][-1] -
                               previousBalance)/previousBalance)*100
            testResults['BotPerformance'].append(
                BotPerformance + previousPerformance)
            previousBalance = self.wallet.balanceEUR+self.wallet.balanceBTC*price
            testResults['CumulativeBotPerformance'] += BotPerformance
            testResults['CumulativeBtcPerformance'] += BtcPerformance
            previousPerformance = BotPerformance

        # logs test results
        testResults['CumulatedGains'] = testResults['BalanceOverTime'][-1] - \
            testResults['BalanceOverTime'][0]
        testResults['TotalGains'] = testResults['CumulatedGains'] - \
            testResults['Fees']

        return testResults

    def updateParameters(self, parameters):
        self.strategy.vars = parameters
