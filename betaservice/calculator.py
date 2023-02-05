import csv, math
from typing import List, Dict, Any
from datetime import timedelta
from collections import defaultdict
from decimal import Decimal
import datetime
import bisect

##############################################
#
#  Helper functions
#
##############################################
def sToDate(s):
    try:
        m, d, y = s.split("/")
        return datetime.date(*map(int,[y,m,d]))
    except (TypeError, ValueError):
        return None


def makeDateList(sDate, endDate):
    delta = endDate - sDate
    t = [sDate + timedelta(days=d) for d in range(delta.days + 1)]
    return filter(lambda x: datetime.date.isoweekday(x) < 6, t)


def getDateList(dates, enddate, duration):
    b = bisect.bisect_left(dates, enddate)
    return dates[b-duration if b > duration else 0:b]


def readfromcsv(datapath):
    res = defaultdict(dict)
    f = open(datapath, 'r')
    rows = csv.DictReader(f)
    for r in rows:
        res[sToDate(r["Date"])][r["Ticker"]] = Decimal(r["ClosePrice"])   # assumption here is the data well defined. Would need sanitizing and validation in real life.
    return res

#################################################

class BusinessException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        pass


def dailyReturn(price_t0, price_t1):
    return math.log(1 + (price_t1 - price_t0) / price_t0)


class Calculator:
    def __init__(self, cache=None):
        self.cache = cache

    def calcVariance(self, values):
        if not values or len(values) < 2:  # assumption here is duration will always be more than 1 day
            raise BusinessException("Bad Values", RuntimeError)   # basic validation but need to expand
        count = len(values)
        _avg = math.fsum(values) / count
        numerator = 0
        for idx in range(1, count):
            dr = dailyReturn(values[idx-1], values[idx])
            numerator += (dr - _avg)**2

        return numerator / (count - 1)

    def calcCovariance(self, tkr_values, base_values):
        if not (tkr_values and base_values) or min(len(tkr_values), len(base_values)) < 2:
            raise BusinessException("Bad Values", RuntimeError)
        tkr_count = len(tkr_values)    # assumption here is len(tkr_values) == len(base_values)
        bs_count = len(base_values)
        tkr_avg = math.fsum(tkr_values) / tkr_count
        bs_avg  = math.fsum(base_values) / bs_count
        numerator = 0
        for idx in range(1,min(tkr_count,bs_count)): # naive guard against IndexError due to lack of time. needs to be reviewed.
            tk_dr = dailyReturn(tkr_values[idx-1], tkr_values[idx])
            bs_dr = dailyReturn(base_values[idx - 1], base_values[idx])
            numerator += (tk_dr - tkr_avg) * (bs_dr - bs_avg)

        return numerator / (min(tkr_count, bs_count) - 1)

    def calcBeta(self, ticker: str, tickerBaseline: str, startDate: str, endDate: str, betaDurationDays: int):
        result = {}
        startDate = sToDate(startDate)
        endDate = sToDate(endDate)
        dateSeries = makeDateList(startDate, endDate)

        for dt in dateSeries:
            _tkr_values = self.cache.getValsForDates(ticker, dt, betaDurationDays)
            _base_values = self.cache.getValsForDates(tickerBaseline, dt, betaDurationDays)
            _var = self.calcVariance(_tkr_values)
            _covar = self.calcCovariance(_tkr_values, _base_values)
            result[dt] = _covar / _var

        return result


class Cache:  # Simple DoD implementation of the cache.
    # This implementation of cache uses python dictionary.
    # The structure is demonstrated below with gaps in data highlighted.
    # Given the specific nature of this data, the date::ticker key approach allows for lateral scaling without increasing lookup time complexity
    # Also allows to initialize from the data source or locally
    sampleData = {
                "2021-01-02": {"MSFT": 125, "YHO": 300, "F": 250,},
                "2021-01-03": {"MSFT": 125, "YHO": 300, "ABC": 250 },
                "2021-01-05": {"MSFT": 125, "YHO": 300, "F": 250, "ZZZ": 0.01},
                "2021-01-03": {"MSFT": 125, "YHO": 300, "F": 250},
            }

    def __init__(self, datapath=None, initData=None):
        self._cache = readfromcsv(datapath) if datapath else initData
        self.sortedkeys = sorted(self._cache.keys())

    def getValsForDates(self, ticker, enddt, duration):
        result = []
        datekeys = getDateList(self.sortedkeys, enddt, duration)
        for d in datekeys:
            result.append(self._cache[d].get(ticker, 0))  # working assumption here is each date has a ticker
        return result


class Service:
    def __init__(self, calc=None, cache=None):
        self.cache = cache or Cache()
        self.calculator = calc or Calculator(self.cache)

    def calcBeta(self, ticker: str, tickerBaseline: str, startDate: str, endDate: str, betaDurationDays: int) -> List:
        result =  self.calculator.calcBeta(ticker, tickerBaseline, startDate, endDate, betaDurationDays)
        return list(map(lambda x: round(x,4), result.values()))


if __name__ == "__main__":
    cache = Cache(datapath="C:/TEMP/TestMarketData.csv")
    calc = Calculator(cache)
    svc = Service(calc, cache)

    test_data = [
        #Ticker  BaseTicker StartDate     EndDate      Duration
        ["MSFT",  "SPY",    "9/14/2021",  "9/21/2021",    3],
        ["AAPL",  "MSFT",   "9/12/2021",  "9/23/2021",    2],
        ["MSFT",  "AAPL",   "9/12/2021",  "9/23/2021",    2],
        ["NVDA",  "SPY",    "9/22/2021",  "9/22/2021",    2],
        ["MSFT",  "SPY",    "9/23/2020",  "9/22/2021",  252],
        ["AAPL",  "MSFT",   "9/23/2020",  "9/22/2021", 1260],
        ["NVDA",  "SPY",    "9/22/2021",  "9/22/2021",  252],
    ]
    for use_case in test_data:
        result = svc.calcBeta(*use_case)
        print(f"{use_case=}:\t{result=}")
