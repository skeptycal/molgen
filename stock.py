# Utilities for stock and option quotes
# Copyright (c) 2020-2021 Michael Treanor
# MIT License. See license.txt

import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

now = dt.datetime.now()
default_ma = 50
default_ema = 30


def Override():
    '''
    Activate yahoo finance workaround
    '''
    yf.pdr_override()


def SMA_string(ma=default_ma):
    return "SMA_" + str(ma)


def EMA_string(ema=default_ema):
    return "EMA_" + str(ema)


def MakeDT(m=now.month, d=now.day, y=now.year,  tz=now.tzinfo) -> dt.datetime:
    '''
    Return a datetime object representing
    the given month, day,  year, and timezone.
    Uses the current values by default.
    '''
    return dt.datetime(y, m, d, tzinfo=tz)


def AddSMA(df, ma=default_ma, drop_initial_rows=True):
    df[SMA_string(ma)] = df.iloc[:, 4].rolling(window=ma).mean()
    if drop_initial_rows:
        df = df.iloc[ma:]


def AddEMA(df, ema, drop_initial_rows=True, adjust=True):
    df[EMA_string(ema)] = df.iloc[:, 4].ewm(span=ema, adjust=adjust).mean()
    if drop_initial_rows:
        df = df.iloc[ema:]


default_ticker_prompt_text = "Enter a stock symbol ('quit' to stop): "


def TickerPrompt(s=default_ticker_prompt_text):
    '''
    Returns CLI input text for ticker symbol.
    '''
    return input(s)


# Set default start time for data sample
start = MakeDT()
