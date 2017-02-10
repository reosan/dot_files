#!/usr/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas.tseries.offsets as offsets
import matplotlib.finance as mpf
import sys
import threading

from modules.plot_def import *

SPAN_s = 13
SPAN_m = 21
SPAN_l = 13
SPAN_ll = 30
HL_BAND_PERIOD = 5

if len(sys.argv) < 2:
    print('Usage: python3 ' + sys.argv[0] + ' quotes.csv [ohlc]')
    exit(1)
    
csv = pd.read_csv(sys.argv[1])
usdjpy = csv_to_df(csv)
ohlc = TF_ohlc(usdjpy)
tohlc = ohlc_to_tohlc(ohlc) 
ax = plt.subplot()


close = ohlc['Close']

plot_ohlc(sys.argv, close, ax, tohlc, SPAN_s, SPAN_m, SPAN_l, SPAN_ll, HL_BAND_PERIOD)

ax.grid() #グリッド表示    
plt.legend()

plt.show()
#plt.savefig('image.png')
