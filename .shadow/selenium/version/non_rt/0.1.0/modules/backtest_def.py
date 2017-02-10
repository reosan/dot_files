import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas.tseries.offsets as offsets
import matplotlib.finance as mpf
import sys
import threading

import modules.colors as C


def iMA(df, ma_period, ma_shift=0, ma_method='EMA', applied_price='Close'):
    if ma_method == 'SMA':    
        return df[applied_price].rolling(ma_period).mean().shift(ma_shift)
    elif ma_method == 'EMA':
        return df[applied_price].ewm(span=ma_period).mean().shift(ma_shift)
    elif ma_method == 'SMMA':
        return df[applied_price].ewm(alpha=1/ma_period).mean().shift(ma_shift)
    elif ma_method == 'LWMA':
        y = pd.Series(0.0, index=df.index)
        for i in range(len(y)):
            if i<ma_period-1: y[i] = 'NaN'
            else:
                y[i] = 0
                for j in range(ma_period):
                    y[i] += df[applied_price][i-j]*(ma_period-j)
                y[i] /= ma_period*(ma_period+1)/2
        return y.shift(ma_shift)
    else: return df[applied_price].copy().shift(ma_shift)

'''    
def BuyEntry(i): # 買いシグナル
    global EMA_S, EMA_M
    return EMA_S[i] > EMA_M[i] and EMA_S[i-1] <= EMA_M[i-1]
def SellEntry(i): # 売りシグナル
    global EMA_S, EMA_M
    return EMA_S[i] < EMA_M[i] and EMA_S[i-1] >= EMA_M[i-1]
def BuyExit(i): # 買いポジション決済シグナル
    return SellEntry(i)
def SellExit(i): # 売りポジション決済シグナル
    return BuyEntry(i)
'''    
