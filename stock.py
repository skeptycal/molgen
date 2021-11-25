# Utilities for stock and option quotes
# Copyright (c) 2020-2021 Michael Treanor
# MIT License. See license.txt

import datetime as dt


def MakeDT(m, d, y: int) -> dt.datetime:
    return dt.datetime(y, m, d)


def AddSMA(df, ma, drop):
    smaString = "SMA_" + str(ma)
    df[smaString] = df.iloc[:, 4].rolling(window=ma).mean()
    if drop:
        df = df.iloc[ma:]


def AddEMA(df, ema, drop):
    emaString = "EMA_" + str(ema)
    df[emaString] = df.iloc[:, 4].ewm(span=ema, adjust=False).mean()
    if drop:
        df = df.iloc[ema:]


stockPrompt = input("Enter a stock symbol ('quit' to stop): ")

startyear = 2020
startmonth = 1
startday = 1

ma = 50
smaString = "SMA_" + str(ma)
ema = 30
emaString = "EMA_" + str(ema)

now = dt.datetime.now()

# Set start time for data sample
start = MakeDT(startmonth, startday, startyear)
