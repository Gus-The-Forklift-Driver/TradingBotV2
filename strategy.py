class buyTheRed:
    # this strategy buys when the price is dropping and sells when it's going up
    def __init__(self, parameters={"consecutiveGreen": 1, "consecutiveRed": 2, "BuyMultiplier": 50, 'SellMultiplier': 50}):
        # these are the parameters of the strategy
        self.vars = parameters

    # this function create an array of values beetween -1 et 1 meaning the buys and sell orders
    def populate_buy_sell(self, marketData):
        dataframe = [0]*marketData.lenght

        consecutiveGreen = 0
        consecutiveRed = 0
        for candle in range(marketData.lenght):
            if int(marketData.close[candle]) > marketData.open[candle]:
                consecutiveGreen += 1
                consecutiveRed = 0
            else:
                consecutiveRed += 1
                consecutiveGreen = 0

            if consecutiveGreen >= self.vars["consecutiveGreen"]:

                amount = (
                    marketData.open[candle] / marketData.close[candle] - 1)*self.vars['SellMultiplier']
                dataframe[candle] = amount

            if consecutiveRed >= self.vars["consecutiveRed"]:
                amount = (
                    marketData.open[candle] / marketData.close[candle] - 1)*self.vars['BuyMultiplier']
                dataframe[candle] = amount
        return dataframe


class diamondHands:
    def __init__(self, parameters={}):
        self.vars = parameters

    def populate_buy_sell(self, marketData):
        dataframe = [0]*marketData.lenght
        dataframe[0] = 1
        return dataframe

class gridTrading:
    def __init__(self,parameters={}):
        self.vars=parameters
    def populate_buy_sell(self,marketData):
        marketData.high
        dataframe= [0]*marketData.lenght
        return dataframe