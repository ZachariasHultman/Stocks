# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 10:11:14 2020

@author: Zacharias Hultman
"""
import numpy as np
import pandas as pd

# import excell. Change if you move the file
data = pd.read_excel("D:\Stocks\Aktie_Utdelning.xlsx",
                     sheet_name='Python', keep_default_na=False)
cols = range(1, 13)
calendar = pd.read_excel("D:\Stocks\Aktie_Utdelning.xlsx",
                         sheet_name='Python', usecols=cols, keep_default_na=False)
stock_rates = pd.read_excel("D:\Stocks\Aktie_Utdelning.xlsx",
                            sheet_name='Python', usecols=[15], keep_default_na=False)

# initialize
amount = 1
dev_tmp = 0
dev = np.empty(len(data.index))
cost = np.empty(len(data.index))


for stock in data.index:
    for month in range(0, len(calendar.columns)):
        #        acess the devidend in month for every stock and * amount of stocks
        dev_tmp = dev_tmp+calendar.iloc[stock, month]*amount
#    save the yearly devidend of the stock
    dev[stock] = dev_tmp
#    acces the row in stock_rates, i.e the rate of the stock *amount of stocks
    cost[stock] = stock_rates.iloc[stock].to_numpy()*amount
#    for next iteration the tmp devidend is set to 0
    dev_tmp = 0

# calculate the total cost of investment and yearly devidend
total_cost = np.sum(cost)
total_dev = np.sum(dev)

print('Total cost is',total_cost)
print('Total devidend is',total_dev)


