class buyTheRed:
    def __init__(self, parameters={"consecutiveGreen": 1, "consecutiveRed": 2, "multiplier": 5}):
        self.vars = parameters

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
                    marketData.open[candle] / marketData.close[candle] - 1)*self.vars["multiplier"]
                dataframe[candle] = amount

            if consecutiveRed >= self.vars["consecutiveRed"]:
                amount = (
                    marketData.open[candle] / marketData.close[candle] - 1)*self.vars["multiplier"]
                dataframe[candle] = amount
        print(dataframe)
        return dataframe
