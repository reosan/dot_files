import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import talib as ta
import sys

SPAN_s = 5
SPAN_m = 9
SPAN_l = 13
SPAN_ll = 30
data = pd.read_csv(sys.argv[1])

stock = []
prices = np.array(stock, dtype='f8')

usdjpy = data[data['<TICKER>'] == 'USDJPY']
del usdjpy['<TICKER>']

usdjpy.index = pd.to_datetime(usdjpy['<YYYY-MM-DD hh:mm:ss>'])

#usdjpy.plot(kind='ohlc')

#df = pd.Series(usdjpy, index=usdjpy.index).resample('B').ohlc()
#mpf.candlestick_ohlc(ax, 

fig = plt.figure()
ax = plt.subplot()

opens = usdjpy['<OPEN>']
highs = usdjpy['<HIGH>']
lows = usdjpy['<LOW>']
closes = usdjpy['<CLOSE>']


mpf.candlestick2_ohlc(ax, opens, highs, lows, closes, width=1, colorup='r', colordown='b', alpha=0.75)


ax.grid() #グリッド表示
#ax.set_xlim(df.index[0].date(), df.index[-1].date()) #x軸の範囲
fig.autofmt_xdate() #x軸のオートフォーマット

#plt.plot(closes)
#ax.plot(closes)
#closes.plot(figure=fig, style='k--')
ewma_S = pd.Seriesewma(closes, span=SPAN_s)
plt.plot(ewma_S)
'''
pd.Series(closes).ewm(span=SPAN_s).mean().plot(style='y')
pd.Series(closes).ewm(span=SPAN_m).mean().plot(style='b')
pd.Series(closes).ewm(span=SPAN_l).mean().plot(style='g')
pd.Series(closes).ewm(span=SPAN_ll).mean().plot(style='r--')
'''

plt.show()

