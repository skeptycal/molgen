

import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

# ******************** Data
startyear = 2020
startmonth = 1
startday = 1
symbols = ["TSLA", "AAPL", "F", "CSCO", "RIG", "ZM"]
# ******************** Data


def MakeDT(m, d, y: int) -> dt.datetime:
    return dt.datetime(y, m, d)


# Activate yahoo finance workaround
yf.pdr_override()

now = dt.datetime.now()

start = MakeDT(startyear, startmonth, startday)

df = pdr.get_data_yahoo(symbols, start, now)

# print(df.tail())

# print(df.memory_usage())

# ma = 50
# smaString = "SMA_" + str(ma)
# ema = 30
# emaString = "EMA_" + str(ema)

# df[emaString] = df.iloc[:,4].ewm(span=ema,adjust=False).mean()
# df[smaString] = df.iloc[:, 4].rolling(window=ma).mean()

# drop first (ma) entries
# df = df.iloc[ma:]
print(df.tail())

print(df)
