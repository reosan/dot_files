import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas.tseries.offsets as offsets

SPAN_s = 5
SPAN_m = 9
SPAN_l = 13
SPAN_ll = 30

data = pd.read_csv(sys.argv[1])
print(data)
usdjpy = data[data['<TICKER>'] == 'USDJPY']
del usdjpy['<TICKER>']

usdjpy.index = pd.to_datetime(usdjpy['<DTYYYYMMDD>'].map(str) + usdjpy['<TIME>'].map(lambda x: "{0:06d}".format(x)))
usdjpy.index += offsets.Hour(8)
del usdjpy['<DTYYYYMMDD>']
del usdjpy['<TIME>']
#usdjpy.index = pd.to_datetime(usdjpy['<YYYY-MM-DD hh:mm:ss>'])

usdjpy_close = usdjpy['<CLOSE>']
usdjpy_close.plot(style='k', label='')
pd.Series(usdjpy_close).ewm(span=SPAN_s).mean().plot(style='y', label=str(SPAN_s))
pd.Series(usdjpy_close).ewm(span=SPAN_m).mean().plot(style='b', label=str(SPAN_m))
pd.Series(usdjpy_close).ewm(span=SPAN_l).mean().plot(style='g', label=str(SPAN_l))
pd.Series(usdjpy_close).ewm(span=SPAN_ll).mean().plot(style='r--', label=str(SPAN_ll))

plt.legend()
plt.show()

