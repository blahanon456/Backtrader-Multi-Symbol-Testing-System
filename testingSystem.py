import os.path
from EarningsBeatStrategySystem import EarningsBeatStrategy
from strategies import *
from pathlib import Path

# class extensions for additional data
class PutEarningsData(bt.feeds.GenericCSVData):
    lines = ('epsestimate', 'epsactual', 'epssurprisepct')
    params = (
        ('dtformat', '%Y-%m-%d'),
        ('Date', 0),
        ('Open', 1),
        ('High', 2),
        ('Low', 3),
        ('Close', 4),
        ('Adj Close', 5),
        ('Volume', 6),
        ('epsestimate', 7),
        ('epsactual', 8),
       ('epssurprisepct', 9)
    )
# class extensions for additional data


directory = "C:\\Users\\jmkre\\PycharmProjects\\financialPythonPractice\\HistoricalData1D"
files = Path(directory).glob('*')

# initiate counts and list for data after running
symbolCount = 0
winnerCount = 0
loserPCT = []
winnerPCT = []
loserCount = 0

# run through the entire folder of data files
for file in files:
    symbolCount+=1
    # put data into backtrader cerebro
    eps_feed = PutEarningsData(dataname=file)
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(25000)
    cerebro.adddata(eps_feed)
    cerebro.addstrategy(EarningsBeatStrategy)

    Symbol = os.path.basename(os.path.normpath(file))
    Symbol = Symbol[:len(Symbol) - 4]
    print('Stock Symbol: ' + Symbol)
    Start = "%.2f" % round(cerebro.broker.getvalue())
    print('Starting Portfolio Value: ' + Start)
    cerebro.run()
    End = "%.2f" % round(cerebro.broker.getvalue(), 2)
    print('Final Portfolio Value: ' + End)

    # getting the percent change
    pctChangeFloat = float(End) / float(Start) - 1
    if(pctChangeFloat > 0):
        winnerCount+=1
        winnerPCT.append(pctChangeFloat)
    else:
        loserCount+=1
        loserPCT.append(pctChangeFloat)
    pctChange = "{:.2%}".format(pctChangeFloat)

    print("Percent change: " + pctChange)
    print()

# printing winners, losers, and averages
winnerPCTCount = winnerCount / symbolCount
print("This strategy had " + "{:.2%}".format(winnerPCTCount) + " winners")
avgWinnerPCT = sum(winnerPCT)/len(winnerPCT)
print("The average winner: +" + "{:.2%}".format(avgWinnerPCT))
loserPCTCount = loserCount / symbolCount
print("This strategy had " + "{:.2%}".format(loserPCTCount) + " losers")
avgLoserPCT = sum(loserPCT)/len(loserPCT)
print("The average loser: " + "{:.2%}".format(avgLoserPCT))
print()

# printing total portfolio change
portfolioChange = sum(loserPCT + winnerPCT)/len(loserPCT + winnerPCT)
pfChange = "{:.2%}".format(portfolioChange)
if(portfolioChange > 0):
    pfChange = "+" + pfChange
print("Total portfolio change: " + pfChange)





