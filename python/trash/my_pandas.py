import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import sys

SPAN_s = 5
SPAN_m = 9
SPAN_l = 13
SPAN_ll = 30

data = pd.read_csv(sys.argv[1])
usdjpy = data[data['<TICKER>'] == 'USDJPY']
del usdjpy['<TICKER>']

#usdjpy.index = pd.to_datetime(usdjpy['<DTYYYYMMDD>'].map(str) + usdjpy['<TIME>'].map(lambda x: "{0:06d}".format(x)))
#del usdjpy['<DTYYYYMMDD>']
#del usdjpy['<TIME>']
usdjpy.index = pd.to_datetime(usdjpy['<YYYY-MM-DD hh:mm:ss>'])

df = pd.Series(usdjpy, index=usdjpy.index).resample('B').ohlc()
#mpf.candlestick_ohlc(ax, 

usdjpy_close = usdjpy['<CLOSE>']
usdjpy_close.plot(style='k--')
pd.Series(usdjpy_close).ewm(span=SPAN_s).mean().plot(style='y')
pd.Series(usdjpy_close).ewm(span=SPAN_m).mean().plot(style='b')
pd.Series(usdjpy_close).ewm(span=SPAN_l).mean().plot(style='g')
pd.Series(usdjpy_close).ewm(span=SPAN_ll).mean().plot(style='r--')

plt.show()

