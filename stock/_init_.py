# Utilities for stock and option quotes
# Copyright (c) 2020-2021 Michael Treanor
# MIT License. See license.txt

import datetime as dt


def MakeDT(m, d, y: int) -> dt.datetime:
    return dt.datetime(y, m, d)


# run until today's date
now = dt.datetime.now()
