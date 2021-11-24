

import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

# Activate yahoo finance workaround
yf.pdr_override()

# run until today's date
now = dt.datetime.now()

# Query user for ticker (testing)
stock = input("Enter a stock symbol ('quit' to stop): ")

startyear = 2020
startmonth = 1
startday = 1

# Set start time for data sample
start = dt.datetime(startyear, startmonth, startday)

df = pdr.get_data_yahoo(stock, start, now)

print(df.tail())

print(df.memory_usage())

ma = 50
smaString = "SMA_" + str(ma)
ema = 30
emaString = "EMA_" + str(ema)

# df[emaString] = df.iloc[:,4].ewm(span=ema,adjust=False).mean()
df[smaString] = df.iloc[:, 4].rolling(window=ma).mean()
df = df.iloc[ma:]
print(df.tail())

print(df)
