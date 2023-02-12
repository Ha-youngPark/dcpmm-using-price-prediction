import math
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass


# Data
price_data = pd.read_csv('simulation\dataset\historical-price.csv') 
# input_data = pd.read_csv('simulation\dataset\input.csv')

# Actual price
# arr_actualPrice = [15.866826, 16.196163, 16.04278, 16.035629, 16.34881, 15.891587, 16.773933, 17.336815, 17.130074, 17.431831, 17.448421, 17.595446, 17.509596, 16.557695, 16.599548, 15.405629, 15.883814, 15.765773, 15.573571, 15.198955]
arr_actualPrice = price_data['Close']

# Random inputAmount of X 
arr_randomInputAmount = [2.04, 2.00, 1.14, -0.24, 1.73, -0.20, 0.20, 0.29, 2.21, -0.18, -1.18, 0.09, 0.18, 0.24, -0.74, -0.28, 1.56, -0.72, -0.74, -1.32]
# arr_randomInputAmount = input_data['Input']

@dataclass
class Trade:  
    reserveX = 10
    reserveY = 158.668261
    arr_reserveX = [reserveX]
    arr_reserveY = [reserveY]
    
    k = reserveX * reserveY
    cnt_k = 0 # index of k
    arr_k = [k]

    poolPrice = round(reserveY / reserveX,7)
    arr_poolPrice = [poolPrice]

    cnt_inputAmount = 0
    inputAmount = arr_randomInputAmount[cnt_inputAmount]  # inputAmount of X
    arr_inputAmountX = []

    outputAmount = 0
    arr_inputAmountY = []
    arr_outputAmount = []

    cnt_actualPrice = 1
    actualPrice = arr_actualPrice[cnt_actualPrice]

    # For calculating impermanent loss
    arr_hold = []
    arr_provideLiquidity = []
    arr_impermanentLoss = []
    

# total simulation count
count = 20


def calculateOutputAmount(trade):
    # Calculate output amount
    trade.outputAmount = -(trade.arr_k[trade.cnt_k] - (trade.reserveX + trade.inputAmount)*trade.reserveY)/(trade.reserveX + trade.inputAmount)
    if trade.inputAmount > 0:
        trade.arr_outputAmount.append(trade.outputAmount)
    print("Output amount: {}".format(trade.outputAmount))
    


def renewReserves(trade):
    trade.reserveX = trade.reserveX + trade.inputAmount
    trade.reserveY = trade.reserveY - trade.outputAmount
    trade.arr_reserveX.append(trade.reserveX)
    trade.arr_reserveY.append(trade.reserveY)
    print("ReserveX: {}".format(trade.reserveX))
    print("ReserveY: {}".format(trade.reserveY))
    
    

def renewPoolPrice(trade):
    trade.poolPrice = round(trade.reserveY / trade.reserveX,6)
    trade.arr_poolPrice.append(trade.poolPrice)
    print("Pool price: {}".format(trade.poolPrice))


def renewActualPrice(trade):
    trade.actualPrice = arr_actualPrice[trade.cnt_actualPrice]
    print("Actual price: {}".format(trade.actualPrice))


def calculateImpermanentLoss(trade):
    hold = (10 * trade.actualPrice) + 158.668261
    trade.arr_hold.append(hold)
    provideLiquidity = (trade.reserveX * trade.actualPrice) + trade.reserveY
    trade.arr_provideLiquidity.append(provideLiquidity)
    impermanentLoss = hold - provideLiquidity
    trade.arr_impermanentLoss.append(impermanentLoss)
    print("Impermanent loss: {}".format(impermanentLoss))


def renewInputAmount(trade):
    if(trade.poolPrice != trade.actualPrice):
        # Arbitrage input
        expectedReserveX = math.sqrt(trade.arr_k[trade.cnt_k]/trade.actualPrice)
        trade.inputAmount = expectedReserveX - trade.reserveX
        print("Nextinput amount: {}".format(trade.inputAmount))
    else:
        # Random input
        trade.cnt_inputAmount += 1
        trade.inputAmount = arr_randomInputAmount[trade.cnt_inputAmount]
        print("Input amount: {}".format(trade.inputAmount))
        #
        trade.cnt_actualPrice += 1
        print("cnt_actualPrice:", trade.cnt_actualPrice)
        # Impermanent loss
        calculateImpermanentLoss(trade)


def renewK(trade):
    k = trade.reserveX * trade.reserveY
    trade.arr_k.append(k)
    trade.cnt_k += 1
    print("k : {}".format(k))


def sellX(trade):
    # If inputAmount is bigger than 0, Sell X and buy Y.
    print("Input amount : {}".format(trade.inputAmount))
    trade.arr_inputAmountX.append(trade.inputAmount)
    
    # Output amount
    calculateOutputAmount(trade)

    # Renew reserves
    renewReserves(trade)

    # Renew pool price
    renewPoolPrice(trade)

    # Renew actual price
    renewActualPrice(trade)
    
    # Renew input amount
    renewInputAmount(trade)
    
    # Renew k value
    renewK(trade)


def sellY(trade):
    # If inputAmount is smaller than 0, Sell Y and buy X.
    print("Input amount : {}".format(trade.inputAmount))

    # Output amount
    calculateOutputAmount(trade)

    # Renew reserves
    renewReserves(trade)

    # Renew pool price
    renewPoolPrice(trade)

    # Renew actual price
    renewActualPrice(trade)

    # Renew input amount
    renewInputAmount(trade)

    # Renew k value
    renewK(trade)
 

def simulation(count, trade):
    for i in range(0, count):
        print("----------------------------------------------------------------------")
        print("{}".format(i))
        if trade.inputAmount > 0:
            sellX(trade)
        elif trade.inputAmount < 0:
            sellY(trade)

def drawPlot(trade):
    plt.figure(figsize=(12,6))
    plt.title('CPMM Impermanent loss')
    plt.ylabel('Value (Unit: ETH)')
    plt.xlabel('Count')
    plt.plot(trade.arr_impermanentLoss, label = 'Impermanent loss')
    plt.grid()
    plt.legend(loc = 'best')
    # plt.savefig('cpmm-il.png')
    plt.show()



# Run simulation 
trade = Trade()
simulation(count, trade)

# Plot
drawPlot(trade)