import backtrader as bt


class EarningsBeatStrategy(bt.Strategy):

    def __init__(self):
        self.epsestimate = self.datas[0].epsestimate
        self.epsactual = self.datas[0].epsactual
        self.epssurprisepct = self.datas[0].epssurprisepct
        self.close = self.datas[0].close

    def next(self):
        if self.epsestimate[0] < self.epsactual[0]:
            self.buy(size=10)
            self.sell(exectype=bt.Order.StopTrail, trailpercent=.10, size = 10)


