import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas.tseries.offsets as offsets
import matplotlib.finance as mpf

def csv_to_df(csv):
    usdjpy = csv[csv['<TICKER>'] == 'USDJPY']
    del usdjpy['<TICKER>']
    usdjpy.index = pd.to_datetime(usdjpy['<DTYYYYMMDD>'].map(str) + usdjpy['<TIME>'].map(lambda x: "{0:06d}".format(x)))
    usdjpy.index += offsets.Hour(8)
    del usdjpy['<DTYYYYMMDD>']
    del usdjpy['<TIME>']
    usdjpy.columns = ['Open', 'High', 'Low', 'Close']
    return usdjpy


def ohlc_to_tohlc(ohlc):
    t = np.arange(1,len(ohlc)+1).reshape((len(ohlc),1))
    tohlc = np.hstack((t, ohlc.values))
    return tohlc


def TF_ohlc(df, tf='Min'):
    x = df.resample(tf).ohlc()
    ret = pd.DataFrame({'Open': x['Open']['open'],
                       'High': x['High']['high'],
                       'Low': x['Low']['low'],
                       'Close': x['Close']['close']},
                       columns=['Open','High','Low','Close'])
    return ret.dropna()


def plot_ohlc(args, close, ax, tohlc, SPAN_s, SPAN_m, SPAN_l, SPAN_ll, HL_BAND_PERIOD):
    if len(args) >= 3 and args[2] == 'ohlc':
        mpf.candlestick_ohlc(ax, tohlc, width=0.7, colorup='blue', colordown='red', alpha=0.5)
        pd.Series(close).ewm(span=SPAN_s).mean().plot(style='y', label=str(SPAN_s), use_index=False)
        pd.Series(close).ewm(span=SPAN_m).mean().plot(style='c', label=str(SPAN_m), use_index=False)
        pd.Series(close).ewm(span=SPAN_l).mean().plot(style='g', label=str(SPAN_l), use_index=False)
        #pd.Series(close).ewm(span=SPAN_ll).mean().plot(style='r--', label=str(SPAN_ll), use_index=False)
        #pd.Series(close).rolling(HL_BAND_PERIOD).max().plot(style='0.5', label='H', use_index=False)
        #pd.Series(close).rolling(HL_BAND_PERIOD).min().plot(style='0.5', label='L', use_index=False)

    else: 
        close.plot(style='k:', label='')
        pd.Series(close).ewm(span=SPAN_s).mean().plot(style='y', label=str(SPAN_s))
        pd.Series(close).ewm(span=SPAN_m).mean().plot(style='c', label=str(SPAN_m))
        pd.Series(close).ewm(span=SPAN_l).mean().plot(style='g', label=str(SPAN_l))
        #pd.Series(close).ewm(span=SPAN_ll).mean().plot(style='r--', label=str(SPAN_ll))
        #pd.Series(close).rolling(HL_BAND_PERIOD).max().plot(style='0.5', label='H')
        #pd.Series(close).rolling(HL_BAND_PERIOD).min().plot(style='0.5', label='L')
        
            # color b,g,r,c,m,y,k,w : '0.75' : '#eeefff'
