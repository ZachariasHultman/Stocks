# -*- coding: utf-8 -*-
"""
Created on Fri Jun  18 17:44:14 2020

@author: Zacharias Hultman
"""
import numpy as np
import pandas as pd
from pandas import ExcelWriter
import networkx as nx
import matplotlib.pyplot as plt
import math

def build_graph(start, bank, excell_data, graph, best_stock):
    global max_dev
    global hidden_bank
    global magic_number
    global total_amount_stocks
    global history
    for stock in excell_data.index:
        # reset the best_stock when a new path from origin is started
        if start == 0:
            best_stock = []
       # check if you've already have bought the max amount if this stock
        if best_stock.count(excell_data.iloc[stock, 0]) < magic_number:
            dev = 0
            for month in range(0, len(calendar.columns)):
                # acess the devidend in month for every stock
                dev = dev+calendar.iloc[stock, month]
                
            # calculate the total yearly devidend
            dev_tot = np.round(start+dev, 2)
            bank_tmp = bank
            # calc the cost
            cost = stock_rates.iloc[stock].to_numpy()
            # buy the stock
            bank_tmp = bank_tmp-cost
            # did you afford it? if not continue to the next stock and try again
            if bank_tmp >= 0:
                best_stock.append(excell_data.iloc[stock, 0])
                # the key attribute works as name info.
                graph.add_node(dev_tot)
                # add weighted edge from where you were to to stock you just bought
                graph.add_weighted_edges_from(
                    [(start, dev_tot, cost)], key=excell_data.iloc[stock, 0])
                # save the maximum devidend as a global variable
                if dev_tot >= max_dev:
                    max_dev = dev_tot
                # add the bought stock to the stack
                history.append(list(best_stock))
                # recursively call the function again, start in the just bought stock
                build_graph(dev_tot, bank_tmp, excell_data, graph, best_stock)

                if len(history) != 0:
                    best_stock = history.pop()
                else:
                    best_stock = []

    # if there are money left after maximum amount of stocks bought, reset the amount
    # and buy as much stocks as the magic number allows again
    if bank > 0 and hidden_bank.count(bank) < 1 and start != 0 and graph.out_degree(start) < (total_amount_stocks-1):
        hidden_bank.append(bank)
        # remove the history since there are money left
        if len(history) != 0:
            history.pop()
        # kanske kom på ett sätt att lägga in start i best_stock så man inte köper samma direkt igen, kanske?  
        best_stock = []
        # recursively call the function again, start in the just bought stock
        build_graph(start, bank, excell_data, graph, best_stock)


def find_cheapest_edge(edge_data):
    #finds the cheapest edge
    #in: 'networkx.classes.coreviews.AtlasView'
    #out: string
    cheapest_stock = math.inf
    for k in edge_data:
        if edge_data[k]['weight'] <= cheapest_stock:
            ultimate_stock = edge_data[k]['key']
    return ultimate_stock

def gen_data_to_excell(stocks,excell_data,file_loc):
    writer=ExcelWriter(file_loc)
    for stock in excell_data.index:
        amount=stocks.count(excell_data.iloc[stock, 0])
        df=pd.DataFrame({excell_data.iloc[stock, 0]:[amount]})
        df.to_excel(writer,'Result',index=stock)
        writer.save()
        
        
        
        

# import excell. Change if you move the file
file_location = "D:\Stocks\Aktie_Utdelning.xlsx"
file_location_write = "D:\Stocks\Result_optimized_bank.xlsx"

data = pd.read_excel(file_location,
                     sheet_name='Python', keep_default_na=False)
cols = range(1, 13)
calendar = pd.read_excel(file_location,
                         sheet_name='Python', usecols=cols, keep_default_na=False)
stock_rates = pd.read_excel(file_location,
                            sheet_name='Python', usecols=[15], keep_default_na=False)

data_write = pd.read_excel(file_location_write,
                     sheet_name='Result', keep_default_na=False)
# The amount of money i have to buy for
bank = 800
# initialize
magic_number = 2
# first node dev is 0 since nothing has been bought, and maximum devdidend is now 0 since no devidend yet
start = 0
max_dev = 0
# initialize the graoh
graph = nx.MultiDiGraph()
graph.add_node(start)
# initialize the lists
best_stock = []
ultimate_stock = []
# hidden bank is used in order to not have an infinity loop in build graph
hidden_bank = []
# total amount of stocks
total_amount_stocks = len(data.index)
# initialize the history stack
history = []
# generates all possibe combinations of the given stocks, bank and magical number
build_graph(start, bank, data, graph, best_stock)

# draw graph
#nx.draw(graph, with_labels=True)
#plt.draw()
#plt.show()

# run djikstra to find the cheapest path to the maximum devidend
# path is the nodes
# length is the total cost of the path
length, path = nx.single_source_dijkstra(graph, 0, max_dev)


for n in range(0, len(path)-1):
    #    find the stocks that represents the path
    ultimate_stock.append(find_cheapest_edge(graph[path[n]][path[n+1]]))
    
print("Maximum devidend is : %s kr" % max_dev)
print("Total cost is : %s kr" % length)
print(ultimate_stock)
#print(path)

#denna gör inte riktigt det den ska än
gen_data_to_excell(ultimate_stock,data,file_location_write)

