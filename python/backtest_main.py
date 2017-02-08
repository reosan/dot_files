#!/usr/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas.tseries.offsets as offsets
import matplotlib.finance as mpf
import sys
import threading

from plot_def import *
from backtest_def import *
import colors as C

SPAN_S = 5
SPAN_M= 9
SPAN_L = 13
SPAN_LL = 30
HL_BAND_PERIOD = 5
Spread = 0.003 # スプレッド
Unit = 10000 # 1ロットの通貨単位 == 1万
Lots = 1.0 # 売買ロット数

if len(sys.argv) < 2:
    print('Usage: python3 ' + sys.argv[0] + ' quotes.csv')
    exit(1)
    
csv = pd.read_csv(sys.argv[1])
usdjpy = csv_to_df(csv)
ohlc = TF_ohlc(usdjpy)
tohlc = ohlc_to_tohlc(ohlc)
close = ohlc['Close']

EMA_S = iMA(ohlc, SPAN_S)
EMA_M = iMA(ohlc, SPAN_M)
EMA_L = iMA(ohlc, SPAN_L)
EMA_LL = iMA(ohlc, SPAN_LL)
def BuyEntry(i): # 買いシグナル
    return EMA_S[i] > EMA_M[i] and EMA_S[i-1] <= EMA_M[i-1]
def SellEntry(i): # 売りシグナル
    return EMA_S[i] < EMA_M[i] and EMA_S[i-1] >= EMA_M[i-1]
def BuyExit(i): # 買いポジション決済シグナル
    return SellEntry(i)
def SellExit(i): # 売りポジション決済シグナル
    return BuyEntry(i)

LongPos = pd.Series(0.0, index=ohlc.index) # 買いポジション情報
ShortPos = LongPos.copy() # 売りポジション情報
BuyPrice = SellPrice = 0.0 # 売買価格
BuyLots = SellLots = 0.0 # 売買ロット数
Open = ohlc['Open'] # 始値

for i in range(1,len(ohlc)-2):
    if BuyEntry(i) and LongPos[i] == 0: LongPos[i+1] = Lots # 買いシグナル
    elif BuyExit(i) and LongPos[i] != 0: LongPos[i+1] = 0 # 買いポジション決済
    else: LongPos[i+1] = LongPos[i] # 買いポジション継続  

    if SellEntry(i) and ShortPos[i] == 0: ShortPos[i+1] = Lots # 売りシグナル
    elif SellExit(i) and ShortPos[i] != 0: ShortPos[i+1] = 0 # 売りポジション決済
    else: ShortPos[i+1] = ShortPos[i] # 売りポジション継続

BuyPoint = LongPos.diff(1)
SellPoint = ShortPos.diff(1)

LongPL = pd.Series(0.0, index=ohlc.index) # 買いポジションの損益
ShortPL = LongPL.copy() # 売りポジションの損益
# Spread = 0.0002 # スプレッド
# Unit = 100000 # 1ロットの通貨単位
# BuyPrice = SellPrice = 0.0 # 売買価格
# BuyLots = SellLots = 0.0 # 売買ロット数
# Open = ohlcD1['Open'] # 始値

for i in range(1,len(ohlc)):
    if BuyPoint[i] > 0:
        BuyPrice = Open[i]+Spread
        BuyLots = LongPos[i]*Unit
        BuyPoint[i] = BuyPrice
    elif BuyPoint[i] < 0:
        ClosePrice = Open[i]
        LongPL[i] = (ClosePrice-BuyPrice)*BuyLots
        BuyPoint[i] = ClosePrice
    else: BuyPoint[i] = 'NaN'

    if SellPoint[i] > 0:
        SellPrice = Open[i]
        SellLots = ShortPos[i]*Unit
        SellPoint[i] = SellPrice
    elif SellPoint[i] < 0:
        ClosePrice = Open[i]+Spread
        ShortPL[i] = (SellPrice-ClosePrice)*SellLots
        SellPoint[i] = ClosePrice
    else: SellPoint[i] = 'NaN'

Initial = 100000 # 初期資産
Equity = (LongPL+ShortPL).cumsum()+Initial
Equity.plot(figsize=(8,6))
ax = plt.subplot()
ax.grid() #グリッド表示    
plt.legend()

plt.show()
