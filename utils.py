def Average(lst):
    return sum(lst) / len(lst)


def create_smoothed(inputData, smoothRange):
    smoothed = []
    for y in range(len(inputData)):
        values = []
        for x in range(smoothRange):
            if -x + y < 0:
                pass
                # values.append(inputData[0])
            else:
                values.append(inputData[-x + y])
        values.append(inputData[y])
        for x in range(smoothRange):
            if x + y > len(inputData)-1:
                pass
                # values.append(inputData[-1])
            else:
                values.append(inputData[x + y])
        smoothed.append(Average(values))
    return smoothed


class marketData():
    def __init__(self, data):
        self.lenght = len(data)
        self.time = []
        self.open = []
        self.high = []
        self.low = []
        self.close = []
        self.volume = []
        self.trades = []
        for candles in data:
            self.time.append(int(candles[0])/1000)
            self.open.append(float(candles[1]))
            self.high.append(float(candles[2]))
            self.low.append(float(candles[3]))
            self.close.append(float(candles[4]))
            self.volume.append(float(candles[5]))
            self.trades.append(float(candles[8]))
        self.highestPrice = max(self.high)
        self.lowestPrice = min(self.low)
        self.start = self.time[0]
        self.end = self.time[-1]
