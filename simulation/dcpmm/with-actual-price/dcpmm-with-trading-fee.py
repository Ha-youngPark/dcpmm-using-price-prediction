import math
import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import dataclass

# Data
price_data = pd.read_csv('simulation\dataset\historical-price.csv')   

# input_data = pd.read_csv('simulation\dataset\input.csv')

# arr_actualPrice = [15.866826, 16.196163, 16.04278, 16.035629, 16.34881, 15.891587, 16.773933, 17.336815, 17.130074, 17.431831, 17.448421, 17.595446, 17.509596, 16.557695, 16.599548, 15.405629, 15.883814, 15.765773, 15.573571, 15.198955]
arr_actualPrice = price_data['Close']

arr_randomInputAmount = [2.04, 2.00, 1.14, -0.24, 1.73, -0.20, 0.20, 0.29, 2.21, -0.18, -1.18, 0.09, 0.18, 0.24, -0.74, -0.28, 1.56, -0.72, -0.74, -1.32, 0.92, 0.19]
# arr_randomInputAmount = input_data['Input']

@dataclass
class Trade():
    reserveX = 10
    reserveY = 158.66826

    arr_reserveX = [reserveX]
    arr_reserveY = [reserveY]
    
    a = 0
    w = 1

    arr_a = [a]
    arr_w = [w]
    
    k = w * (reserveX - a) * reserveY
    cnt_k = 0
    arr_k = [k]
    
    feeRate = 0.003
    tradingFee = 0

    arr_tradingFeeX = []
    arr_tradingFeeY = []
    arr_tradingFee = []
    
    poolPrice = round(reserveY / reserveX,6)
    arr_poolPrice = [poolPrice]
    
    cnt_randomInputAmount = 0
    inputAmount = arr_randomInputAmount[cnt_randomInputAmount]
    arr_inputAmount = []

    actualInputAmount = 0
    arr_actualInputAmount = []
    
    outputAmount = 0
    arr_outputAmount = []

    actualOutputAmount = 0
    arr_actualOutputAmount = []
    
    cnt_actualPrice = 0
    actualPrice = arr_actualPrice[cnt_actualPrice]
    
    expectedReserveX = 0
    
    isArbitrage = True
    

def calculateTradingFee(trade):
    if(trade.isArbitrage):
        trade.actualInputAmount = trade.inputAmount
        trade.arr_actualInputAmount.append(trade.actualInputAmount)
        print("Actual input amount : {}".format(trade.actualInputAmount))
        
        trade.inputAmount = trade.actualInputAmount / 0.997
        trade.arr_inputAmount.append(trade.inputAmount)
        print("Input amount: {}".format(trade.inputAmount))
        
        trade.tradingFee = trade.inputAmount - trade.actualInputAmount
        trade.arr_tradingFeeX.append(trade.tradingFee)  
        print("Trading fee: {}".format(trade.tradingFee))
        
        trade.tradingFee_XtoY = trade.reserveY - (trade.arr_k[trade.cnt_k] /(trade.w * (trade.reserveX + trade.tradingFee - trade.a)))
        trade.arr_tradingFee.append(trade.tradingFee_XtoY) 
        print("tradingFee_XtoY {}".format(trade.tradingFee_XtoY))
        
    else:     
        trade.tradingFee = trade.inputAmount * trade.feeRate     
        trade.arr_tradingFeeX.append(trade.tradingFee)
        
        trade.actualInputAmount = trade.inputAmount - trade.tradingFee
        trade.arr_actualInputAmount.append(trade.actualInputAmount)
        print("Actual input amount : {}".format(trade.actualInputAmount))
        
        trade.tradingFee_XtoY = trade.reserveY - (trade.arr_k[trade.cnt_k] /(trade.w * (trade.reserveX + trade.tradingFee - trade.a)))
        trade.arr_tradingFee.append(trade.tradingFee_XtoY)


def calculateOutputAmount(trade):
    trade.outputAmount = trade.reserveY - (trade.arr_k[trade.cnt_k] /(trade.w * (trade.reserveX + trade.actualInputAmount - trade.a)))
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
    trade.poolPrice = round((trade.arr_k[trade.cnt_k]/trade.w)*(1/pow(trade.reserveX - trade.a, 2)),6)
    trade.arr_poolPrice.append(trade.poolPrice)
    print("Pool price: {}".format(trade.poolPrice))
    print("Market price: {}".format(trade.actualPrice))


def renewActualPrice(trade):
    trade.cnt_actualPrice += 1
    trade.actualPrice = arr_actualPrice[trade.cnt_actualPrice]
    print("cnt_actualPrice: {}".format(trade.cnt_actualPrice))
    print("Actual price: {}".format(trade.actualPrice))


def renewAandW(trade):
    trade.a = trade.reserveX - (trade.reserveY / trade.actualPrice)
    trade.arr_a.append(trade.a)
    print("a: {}".format(trade.a))
    trade.w = (trade.arr_k[trade.cnt_k] * trade.actualPrice) / math.pow(trade.reserveY,2)
    trade.arr_w.append(trade.w)
    print("w: {}".format(trade.w)) 


def renewInputAmount(i, trade):
    if(trade.poolPrice != trade.actualPrice):
        # Arbitrage input
        trade.isArbitrage = True
        trade.expectedReserveX = trade.arr_reserveX[i-1]
        trade.inputAmount = trade.expectedReserveX - trade.reserveX
        print("Next input amount: {}".format(trade.inputAmount))
    else:   
        # Random input
        trade.isArbitrage = False
        trade.cnt_randomInputAmount += 1
        trade.inputAmount = arr_randomInputAmount[trade.cnt_randomInputAmount]
        print("Next input amount: {}".format(trade.inputAmount))
        
        # Renew market price
        renewActualPrice(trade)
        
        # Renew a and w
        renewAandW(trade)
        
        # Renew pool price
        renewPoolPrice(trade)
 
 
def renewK(trade):
    trade.k = trade.w * (trade.reserveX - trade.a ) * trade.reserveY
    trade.arr_k.append(trade.k)
    print("k : {}".format(trade.k))
    trade.cnt_k += 1            


def calculateOutputAmountY(trade):
    trade.actualOutputAmount = trade.reserveY - (trade.arr_k[trade.cnt_k] /(trade.w * (trade.reserveX + trade.inputAmount - trade.a)))
    trade.arr_actualOutputAmount.append(trade.actualOutputAmount)
    print("Output amount: {}".format(trade.actualOutputAmount))


def calculateTradingFeeY(trade):
    trade.outputAmount = trade.actualOutputAmount / 0.997
    trade.arr_outputAmount.append(trade.outputAmount)
    trade.tradingFee = trade.outputAmount - trade.actualOutputAmount
    trade.arr_tradingFeeY.append(trade.tradingFee)
    trade.arr_tradingFee.append(-trade.tradingFee)
    print("Trading fee Y: {}".format(trade.tradingFee))


def renewReservesY(trade):
    trade.reserveX = trade.reserveX + trade.inputAmount
    trade.reserveY = trade.reserveY - trade.actualOutputAmount
    trade.arr_reserveX.append(trade.reserveX)
    trade.arr_reserveY.append(trade.reserveY)
    print("ReserveX: {}".format(trade.reserveX))
    print("ReserveY: {}".format(trade.reserveY))







def sellX(i, trade):
    print("ReserveX: {}".format(trade.reserveX))
    print("ReserveY: {}".format(trade.reserveY))
    print("Input amount : {}".format(trade.inputAmount))
    trade.arr_inputAmount.append(trade.inputAmount)

    # Trading fee
    calculateTradingFee(trade)
            
    # Output amount
    calculateOutputAmount(trade)
            
    # Renew reserves
    renewReserves(trade)        
            
    # Renew pool price
    renewPoolPrice(trade)
      
    # Renew input amount
    renewInputAmount(i,trade)
                
    # Renew k value
    renewK(trade)
        


def sellY(i, trade):
    print("ReserveX: {}".format(trade.reserveX))
    print("ReserveY: {}".format(trade.reserveY))
    print("Input amount : {}".format(trade.inputAmount))
    
    # Output amount
    calculateOutputAmountY(trade)
       
    # Trading fee
    calculateTradingFeeY(trade)
        
    # Renew reserves
    renewReservesY(trade)
            
    # Renew pool price
    renewPoolPrice(trade)

    # Renew input amount
    renewInputAmount(i, trade)
       
    # Renew k value
    renewK(trade)

    

    


# total simulation count    
count = 20    



def simulation(count, trade):
    for i in range(1,count):
        print("----------------------------------------------------------------------")
        print("{}".format(i))
        if(trade.inputAmount > 0):
            sellX(i, trade)    
        elif(trade.inputAmount < 0):
            sellY(i, trade)
   

def drawPlot(trade):
    plt.figure(figsize=(12,6))
    plt.title('DCPMM Trading fee (Actual price)')
    plt.ylabel('Value (Unit: ETH)')
    plt.xlabel('Count')
    plt.plot(trade.arr_tradingFee, label = 'Trading fee')
    plt.grid()
    plt.legend(loc = 'best')
    # plt.savefig('dcpmm_tf_actual.png')
    plt.show()


# Run simulation
trade = Trade()
simulation(count, trade)

# Plot
drawPlot(trade)
