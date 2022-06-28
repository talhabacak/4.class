# -*- coding: utf-8 -*-
"""
Created on Sat May 23 19:26:22 2022

@author: talha
"""
import pandas as pd
import talib



def getFirstData(path):
    data = pd.read_csv(path,on_bad_lines='skip')
    return data    

def setIndicator(historyClose, historyHigh, historyLow):
    ema9 = talib.EMA(historyClose, 9)
    ema26 = talib.EMA(historyClose, 26)
    ema_diff9 = (ema9-ema26) / ema9
    
    sma200 = talib.SMA(historyClose, 200)
    
    rsi = talib.RSI(historyClose)
    
    adx = talib.ADX(historyHigh, historyLow, historyClose)
    
    di_plus  = talib.PLUS_DM(historyHigh, historyLow)
    di_minus = talib.MINUS_DM(historyHigh, historyLow)
    dx = (di_plus - di_minus) / (di_plus + di_minus)
    
    return ema_diff9, sma200, rsi, adx, dx
    
def writeIndicator(path,ema_diff_9,sma200,rsi,adx,dx,historyClose):
    txt = open(path,"w")
    data = []

    for i in range(len(historyClose)-1,0,-1):
        temp = [ema_diff_9[i],sma200[i],rsi[i],adx[i],dx[i],historyClose[i],historyClose[i-1]]
        if historyClose[i] < historyClose[i-1]:
            temp.append(1)
        else:
            temp.append(0)
        data.append(temp)

    text = ""
    for i in data:
        count = 1
        for j in i:
            if count < len(i):
                text += str(j) + ","
            else:
                text += str(j) + "\n"
            count += 1

    print(len(text))
    txt.write(text)
    txt.close()
    
def runPreprocess(path, pathOut):
    data = getFirstData(path)
    data2 = data.reindex(index=data.index[::-1])
    
    historyClose = data2["close"]
    historyLow = data2["low"]
    historyHigh = data2["high"]
    
    ema_diff_9, sma200, rsi, adx, dx = setIndicator(historyClose, historyHigh, historyLow)
    writeIndicator(pathOut, ema_diff_9, sma200, rsi, adx, dx, historyClose)
    
path = "Poloniex_BTCUSDT_1h.csv"
pathOut = "data_h.txt"
runPreprocess(path, pathOut)

path = "Poloniex_BTCUSDT_1h_test.csv"
pathOut = "data_h_test.txt"
runPreprocess(path, pathOut)

path = "Poloniex_BTCUSDT_d.csv"
pathOut = "data_d.txt"
runPreprocess(path, pathOut)

path = "Poloniex_BTCUSDT_d_test.csv"
pathOut = "data_d_test.txt"
runPreprocess(path, pathOut)
