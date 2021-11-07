import paper


class backendTest():
    def __init__(self, data, strategy):
        self.wallet = paper.wallet()
        self.marketData = data
        self.strategy = strategy

    # run the simulation for a strategy according to given parameters
    def runTest(self):
        self.wallet.balanceEUR = 100
        self.wallet.balanceBTC = 0
        testResults = {'BuyOperations': 0,
                       'SellOperations': 0,
                       'CumulatedGains': 0,
                       'TotalGains': 0,
                       'Fees': 0,
                       'EurOverTime': [],
                       'BtcOverTime': [],
                       'BalanceOverTime': [],
                       'ComparedPerformance': []}
        BuynSell = self.strategy.populate_buy_sell(self.marketData)
        for candle in range(self.marketData.lenght):
            price = self.marketData.close[candle]
            if BuynSell[candle] > 0 and self.wallet.balanceEUR > 0:
                amount = self.wallet.balanceEUR*BuynSell[candle]
                try:
                    fees = self.wallet.buyMarket(price, amount)
                except ValueError:
                    pass
                else:
                    testResults['Fees'] += fees
                    testResults['BuyOperations'] += 1

            elif BuynSell[candle] < 0 and self.wallet.balanceBTC > 0:
                amount = self.wallet.balanceBTC*BuynSell[candle]*-1
                try:
                    fees = self.wallet.sellMarket(price, amount)
                except ValueError:
                    pass
                else:
                    testResults['Fees'] += fees
                    testResults['SellOperations'] += 1
            # logs current progress
            testResults['EurOverTime'].append(self.wallet.balanceEUR)
            testResults['BtcOverTime'].append(self.wallet.balanceBTC)
            testResults['BalanceOverTime'].append(
                self.wallet.balanceEUR+self.wallet.balanceBTC*price)
        # logs test results
        testResults['CumulatedGains'] = testResults['BalanceOverTime'][-1] - \
            testResults['BalanceOverTime'][0]
        testResults['TotalGains'] = testResults['CumulatedGains'] - \
            testResults['Fees']
        return testResults

    def updateParameters(self, parameters):
        self.strategy.vars = parameters
