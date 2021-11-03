class wallet:
    precision = 8

    def __init__(self):
        self.balanceEUR = 100
        self.balanceBTC = 0
        self.makerFee = 0.1
        self.takerFee = 0.1
        self.minimumTradeAmount = 0.00001
        self.minimumOrderSize = 10

    def buyMarket(self, price, EURAmount='max'):
        if EURAmount == 'max':
            EURAmount = self.balanceEUR
        if EURAmount < self.minimumOrderSize:
            raise ValueError("Minimum Order Size reached")
        else:
            fee = (EURAmount/100) * self.makerFee
            BTCAmount = (EURAmount - fee) / price
            if BTCAmount < self.minimumTradeAmount:
                raise ValueError("Trade amount not enough")
            newEurBalance = self.balanceEUR - EURAmount
            if newEurBalance < 0:
                raise ValueError('specified amount too high')
            self.balanceBTC += BTCAmount
            self.balanceEUR = newEurBalance
            return fee

    def sellMarket(self, price, BTCAmount='max'):
        fee = 0
        if BTCAmount == 'max':
            BTCAmount = self.balanceBTC
        if BTCAmount < self.minimumTradeAmount:
            raise ValueError("Trade amount not enough")
        else:
            fee = (BTCAmount/100) * self.takerFee
            EURAmount = (BTCAmount - fee) * price
            newBtcBalance = self.balanceBTC - BTCAmount
            if newBtcBalance < 0:
                raise ValueError('specified amount too high')
            self.balanceEUR += EURAmount
            self.balanceBTC = newBtcBalance
            return fee
