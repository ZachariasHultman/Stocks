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

# The amount of money i have to buy for
bank = 350
# initialize
dev_tmp = 0
dev_high = 0
dev_year = []
best_stock = []
cost = []
amount_bought_stocks = 0

magic_number=20

while True:
    for stock in data.index:
        for month in range(0, len(calendar.columns)):
#            acess the devidend in each month for every stock and add them together to get the yearly dividend
            dev_tmp = dev_tmp+calendar.iloc[stock, month]
#        can you afford to buy the stock?
#       are you allowed to buy it? if not move on to the next
        if bank >= stock_rates.iloc[stock].to_numpy() and best_stock.count(data.iloc[stock, 0])<=magic_number:
#           if the stock you bought gives more devidend, save that as the best stock
            if dev_tmp >= dev_high:
                if dev_high == 0:
                    best_stock.append(data.iloc[stock, 0])
#                   save the yearly devidend of the stock
                    dev_year.append(dev_tmp)
#                   Save the price of the best stock
                    cost.append(stock_rates.iloc[stock].to_numpy())
                else:
                    #delete the prev. best stock, since you have found a better
                    best_stock.pop()
#                   delete the yearly devidend of the prev. best stock
                    dev_year.pop()
#                    delete the cost of the prev. best stock
                    cost.pop()
#                    add the new best stock
                    best_stock.append(data.iloc[stock, 0])
#                    save the yearly devidend of the new best stock
                    dev_year.append(dev_tmp)
#                   Save the price of the best stock
                    cost.append(stock_rates.iloc[stock].to_numpy())
#               update the new highest values
                dev_high = dev_tmp
                print('best stock')
#           if this wasn't the best stock, you shouldn't buy it
            else:
                print('not the best stock')
#        for next iteration the devidend for the stock is set to 0
        dev_tmp = 0
    print('the best stock has been found')
#   since the first buy iteration is done, the highest dev is 0 for next iteration
    dev_high = 0
#    if no more stocks have been bought => end you're done
    if len(best_stock) == amount_bought_stocks:
        break
#    save the amount of stocks that has been bought
    amount_bought_stocks = len(best_stock)
    bank = bank-cost[-1]


# calculate the total cost of investment and yearly devidend
total_cost = np.sum(cost)
total_dev = np.sum(dev_year)

print('Total cost is',total_cost)
print('Total yearly devidend',total_dev)
print('The best stocks are',best_stock)
print('Money left in the BANK',bank)
