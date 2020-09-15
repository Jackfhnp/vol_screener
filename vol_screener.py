import pandas as pd
import talib
import numpy as np

class volatility_screener(object):
    def __init__(self, df, symbol):
        self.df = df
        self.symbol = symbol

    def data_process(self):
        self.df['log_price'] = np.log(self.df['Adj Close'])
        self.df['log_return'] = self.df['log_price'].diff()
        self.df.dropna(inplace=True)

        self.df['log_ret_7'] = talib.SMA(self.df.log_return, timeperiod=7)
        self.df['log_ret_14'] = talib.SMA(self.df.log_return, timeperiod=14)
        self.df['log_ret_60'] = talib.SMA(self.df.log_return, timeperiod=60)
        
        self.df['vol_7'] = talib.STDDEV(self.df.log_return, timeperiod=7)
        self.df['vol_14'] = talib.STDDEV(self.df.log_return, timeperiod=14)
        self.df['vol_60'] = talib.STDDEV(self.df.log_return, timeperiod=60)

        self.df['log_return1'] = self.df.log_return.shift(-1)
        today = self.df.iloc[-2, :]
        return today

    def TWOSTDDEV(self):
        today = self.data_process()
        condition1 = today.log_return1 > today.log_ret_7 +  2*today.vol_7
        condition2 = today.log_return1 < today.log_ret_7 -  2*today.vol_7
        # if condition1 | condition2:
        #     print(f"{self.symbol}'s volatility is 2 STDDEV away from narmal return")
        # else:
        #     print(f"{self.symbol}'s volatility is normal")
        return condition1, condition2

    def THREESTDDEV(self):
        today = self.data_process()
        condition1 = today.log_return1 > today.log_ret_7 + 3*today.vol_7
        condition2 = today.log_return1 < today.log_ret_7 - 3*today.vol_7
        
        # if condition1 | condition2:
        #     print(f"{self.symbol}'s volatility is 3 STDDEV away from narmal return")
        # else:
        #     print(f"{self.symbol}'s volatility is normal")
        return condition1, condition2

    def SIXSTDDEV(self):
        today = self.data_process()
        condition1 = today.log_return1 > today.log_ret_7 + 6*today.vol_7
        condition2 = today.log_return1 < today.log_ret_7 - 6*today.vol_7
        
        # if condition1 | condition2:
        #     print(f"{self.symbol}'s volatility is 6 STDDEV away from narmal return")
        # else:
        #     print(f"{self.symbol}'s volatility is normal")
        return condition1, condition2