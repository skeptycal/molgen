

import pandas as pd
import numpy as np
import yfinance as yf
# import datetime as dt
from pandas_datareader import data as pdr
from stock import *

# Activate yahoo finance workaround
yf.pdr_override()


df = pdr.get_data_yahoo(stockPrompt, start, now)

AddSMA(df, ma, True)
AddEMA(df, ema, False)

print(df)

# df[emaString] = df.iloc[:, 4].ewm(span=ema, adjust=False).mean()
# df[smaString] = df.iloc[:, 4].rolling(window=ma).mean()
# drop first (ma) entries
# df = df.iloc[ma:]

# print(df.tail())

# print(df.memory_usage())
