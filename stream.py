
from ansi import *
from stock import *

Override()

# ******************** Data
symbols = ["TSLA", "AAPL", "F", "CSCO", "RIG", "ZM"]

# ******************** Output:
for symbol in symbols:

    df = pdr.get_data_yahoo(symbol, start, now)
    print(f"{GREEN}{symbol}: {RESET}{df}")
