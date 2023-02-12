import math
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass


# Data
price_data = pd.read_csv('simulation\dataset\historical-price.csv')  
# input_data = pd.read_csv('simulation\dataset\input.csv')


# Actual market price
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
    
    
    feeRate = 0.003
    tradingFee = 0
    arr_tradingFeeX = []
    arr_tradingFeeY = []
    arr_tradingFee = []
    
    # Fee를 제거한 Input
    actualInputAmount = 0
    arr_actualInputAmount = []    

    poolPrice = round(reserveY / reserveX,7)
    arr_poolPrice = [poolPrice]

    cnt_inputAmount = 0
    inputAmount = arr_randomInputAmount[cnt_inputAmount]  # inputAmount of X
    arr_inputAmount = []

    outputAmount = 0
    arr_outputAmount = []
    
    # outputAmount without trading fee
    actualOutputAmount = 0
    arr_actualOutputAmount = []

    cnt_actualPrice = 1
    actualPrice = arr_actualPrice[cnt_actualPrice]

    expectedReserveX = 0
    
    isArbitrage = True
    

# total simulation count
count = 20


def calculateTradingFee(trade):
    if(trade.isArbitrage):
        trade.actualInputAmount = trade.inputAmount 
        trade.arr_actualInputAmount.append(trade.actualInputAmount)
        print("Actual input amount : {}".format(trade.actualInputAmount))

        trade.inputAmount = trade.actualInputAmount / 0.997 
        trade.arr_inputAmount.append(trade.inputAmount)
        
        trade.tradingFee = trade.inputAmount - trade.actualInputAmount
        trade.arr_tradingFeeX.append(trade.tradingFee)
            
        trade.tradingFee_XtoY = -(trade.arr_k[trade.cnt_k] - (trade.reserveX + trade.tradingFee)*trade.reserveY)/(trade.reserveX + trade.tradingFee)
        trade.arr_tradingFee.append(trade.tradingFee_XtoY)
    else:     
        trade.tradingFee = trade.inputAmount * trade.feeRate
        trade.arr_tradingFeeX.append(trade.tradingFee)
        
        trade.actualInputAmount = trade.inputAmount - trade.tradingFee
        trade.arr_actualInputAmount.append(trade.actualInputAmount)
        print("Actual input amount : {}".format(trade.actualInputAmount))
        
        trade.tradingFee_XtoY = -(trade.arr_k[trade.cnt_k] - (trade.reserveX + trade.tradingFee)*trade.reserveY)/(trade.reserveX + trade.tradingFee)
        trade.arr_tradingFee.append(trade.tradingFee_XtoY)



def calculateOutputAmount(trade):
    trade.outputAmount = -(trade.arr_k[trade.cnt_k] - (trade.reserveX + trade.actualInputAmount)*trade.reserveY)/(trade.reserveX + trade.actualInputAmount)
    trade.arr_outputAmount.append(trade.outputAmount)
    print("Output amount: {}".format(trade.outputAmount))
    

def renewReserves(trade):
    trade.reserveX = trade.reserveX + trade.actualInputAmount
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


def renewInputAmount(trade):
    if(trade.poolPrice != trade.actualPrice):
        print("P-Current normal trade")
        # Arbitrage input
        trade.isArbitrage = True
        trade.expectedReserveX = math.sqrt(trade.arr_k[trade.cnt_k]/trade.actualPrice) 
        print("ExpectedReserveX: {}".format(trade.expectedReserveX))
        trade.inputAmount = trade.expectedReserveX - trade.reserveX
        print("Nextinput amount: {}".format(trade.inputAmount))
    else:
        print("P-Current arbitrage trade")
        # Random input
        trade.isArbitrage = False
        trade.cnt_inputAmount += 1
        trade.inputAmount = arr_randomInputAmount[trade.cnt_inputAmount]
        print("Input amount: {}".format(trade.inputAmount))
    
        trade.cnt_actualPrice += 1
    

def renewK(trade):
    k = trade.reserveX * trade.reserveY
    trade.arr_k.append(k)
    trade.cnt_k += 1
    print("k : {}".format(k))


def calculateOutputAmountY(trade):
    trade.actualOutputAmount = - (trade.arr_k[trade.cnt_k] - (trade.reserveX + trade.inputAmount) * trade.reserveY) / (trade.reserveX + trade.inputAmount)
    trade.arr_actualOutputAmount.append(trade.actualOutputAmount)
    print("Actual output amount: {}".format(trade.actualOutputAmount))


def renewTradingFeeY(trade):
    trade.outputAmount = trade.actualOutputAmount / 0.997
    trade.arr_outputAmount.append(trade.outputAmount)
    trade.tradingFee = trade.outputAmount - trade.actualOutputAmount
    trade.arr_tradingFeeY.append(trade.tradingFee)
    trade.arr_tradingFee.append(-trade.tradingFee)
    print("Output amount: {}".format(trade.outputAmount))
    print("Trading fee Y: {}".format(trade.tradingFee))


def renewReservesY(trade):
    trade.reserveX = trade.reserveX + trade.inputAmount
    trade.reserveY = trade.reserveY - trade.actualOutputAmount
    trade.arr_reserveX.append(trade.reserveX)
    trade.arr_reserveY.append(trade.reserveY)
    print("ReserveX: {}".format(trade.reserveX))
    print("ReserveY: {}".format(trade.reserveY))
    

def renewInputAmountY(trade):
    if(trade.poolPrice != trade.actualPrice):
        print("N-Current normal trade")
        # Arbitrage input
        trade.expectedReserveX = math.sqrt(trade.arr_k[trade.cnt_k]/trade.actualPrice)
        print("Expected reserveX: {}".format(trade.expectedReserveX))
        trade.inputAmount = trade.expectedReserveX - trade.reserveX
        print("Nextinput amount: {}".format(trade.inputAmount))
    else:
        print("N-Current arbitrage trade")
        # Random input
        trade.cnt_inputAmount += 1
        trade.inputAmount = arr_randomInputAmount[trade.cnt_inputAmount]
        print("Input amount : {}".format(trade.inputAmount))
        trade.cnt_actualPrice += 1
        
    


def sellX(trade):
    # If inputAmount is bigger than 0, Sell X and buy Y.
    print("ReserveX: {}".format(trade.reserveX))
    print("ReserveY: {}".format(trade.reserveY))    
    print("Input amount : {}".format(trade.inputAmount))
    print("Pool price: {}".format(trade.poolPrice))


    # Calculate trading fee and 
    calculateTradingFee(trade)
        
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
    print("Input amount : {}".format(trade.inputAmount))
    trade.arr_inputAmount.append(trade.inputAmount)
    
    # Output amount
    calculateOutputAmountY(trade)

    # Trading fee
    renewTradingFeeY(trade)

    # Renew reserves
    renewReservesY(trade)

    # Renew pool price
    renewPoolPrice(trade)
    
    # Renew actual price
    renewActualPrice(trade)
    
    # Renew input amount
    renewInputAmountY(trade)
    
    # Renew k value
    renewK(trade)




def simulation(count, trade):
    for i in range(0,count):
        print("----------------------------------------------------------------------")
        print("{}".format(i))
        if(trade.inputAmount > 0):
            sellX(trade)
        elif(trade.inputAmount < 0):
            sellY(trade)            


def drawPlot(trade):
    plt.figure(figsize=(12,6))
    plt.title('CPMM Trading fee')
    plt.ylabel('Value (Unit: ETH)')
    plt.xlabel('Count')
    plt.plot(trade.arr_tradingFee, label = 'Trading fee')
    plt.grid()
    plt.legend(loc = 'best')
    # plt.savefig('cpmm_tf.png')
    plt.show()


# Run simulation 
trade = Trade()
simulation(count, trade)

# Plot
drawPlot(trade)