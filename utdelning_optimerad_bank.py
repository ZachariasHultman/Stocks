#För att hitta upprepningar funkar inte så bra just nu
#axfood läggs inte till i max_dev_hist. Varför???
#om magic number > 1 blir det för dyrt????
#funkar inte om man byter ordning i listan i excell. Varför i fan????


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
import tools

def build_magic_graph(start, bank, excell_data, graph, best_stock):
    global max_dev
    global magic_number_init
    global magic_number
    global cheapest_stock
    global best_stock_history
#    global best_stock_history_tmp
    global bank_init
    global history
    global max_dev_hist
    global flagsator
    stock=-1
    while True:
        stock=stock+1
        if stock>max(excell_data.index):
            break
        # reset the best_stock when a new path from origin is started
        if start == 0:
            bank=bank_init
            best_stock = []
            best_stock_tmp=[]
            magic_number=magic_number_init
        # calc the cost
        cost = stock_rates.iloc[stock].to_numpy()
        # buy the stock
        bank_tmp = bank-cost
       # check if you've already have bought the max amount if this stock
        # did you afford it? if not continue to the next stock and try again
        if len(list(filter(lambda i: i['name'] == excell_data.iloc[stock, 0] , best_stock))) < magic_number and bank_tmp >= 0:          
            best_stock.append({'name':excell_data.iloc[stock, 0],'index':stock})
            best_stock=sorted(best_stock, key=lambda i: i['index'])
#            best_stock_tmp.append({'name':excell_data.iloc[stock, 0],'index':stock,'bank':bank,'bank_tmp':bank_tmp})
#            best_stock_tmp=sorted(best_stock_tmp, key=lambda i: i['index'])
            hist_ind=0
            counter=0
            for b in best_stock:
                counter=counter+1
                hist_ind=hist_ind+(100**(counter))*b.get('index')
            if hist_ind in hist_ind_set:
                best_stock=tools.del_first_occurence(best_stock,stock)
#                best_stock_tmp=tools.del_first_occurence(best_stock_tmp,stock)
                continue          
            dev = 0            
            for month in range(0, len(calendar.columns)):
                # acess the devidend in month for every stock
                dev = dev+calendar.iloc[stock, month]   
            # calculate the total yearly devidend
            dev_tot = np.round(start+dev)
            # save the maximum devidend as a global variable
            if dev_tot >= max_dev:
                if dev_tot==max_dev:
                    max_dev_hist.append(list(best_stock))
                elif dev_tot>max_dev:
                    max_dev_hist=[]
                    max_dev_hist.append(list(best_stock))
                max_dev = dev_tot
            # add the bought stock to the stack
            best_stock_history.append(list(best_stock))
#            best_stock_history_tmp.append(list(best_stock_tmp))
            history.append(list(best_stock))
            hist_ind_set.add(hist_ind)
            # the key attribute works as name info.
            graph.add_node(dev_tot)
            # add weighted edge from where you were to to stock you just bought
            graph.add_weighted_edges_from(
                [(start, dev_tot, cost)], key=excell_data.iloc[stock, 0])
            if bank_tmp >= cheapest_stock:
                # recursively call the function again, start in the just bought stock
                build_magic_graph(dev_tot, bank_tmp, excell_data, graph, best_stock)
            if len(list(filter(None,best_stock)))!=0:
                best_stock=best_stock_history.pop()
#                best_stock_tmp=best_stock_history_tmp.pop()
            if len(list(filter(None,best_stock)))!=0:
                best_stock=tools.del_first_occurence(best_stock,stock)
#                best_stock_tmp=del_first_occurence(best_stock_tmp,stock)
#                best_stock_tmp=[i for i in best_stock_tmp if not (i['index']==stock)]
        elif stock == max(excell_data.index) and bank>cheapest_stock and len(list(filter(None,best_stock)))==total_amount_stocks*magic_number:
            magic_number=magic_number+1
            print('Increase magic number. New magic:' , magic_number)
            build_magic_graph(start, bank, excell_data, graph, best_stock,best_stock_tmp)
            magic_number=magic_number-1
            print('Decrease magic number. New magic:' , magic_number)


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
bank = 500
bank_init=bank
# initialize
magic_number_init = 1
magic_number = magic_number_init
# first node dev is 0 since nothing has been bought, and maximum devdidend is now 0 since no devidend yet
start = 0
max_dev = 0
# initialize the graoh
graph = nx.MultiDiGraph()
graph.add_node(start)
# initialize the lists
best_stock = []
ultimate_stock = []
# total amount of stocks
total_amount_stocks = len(data.index)
#find cheapest stock value
cheapest_stock=math.inf
for stock in data.index:
    cost_tmp = stock_rates.iloc[stock].to_numpy()
    if cost_tmp < cheapest_stock:
        cheapest_stock=cost_tmp

# initialize the best_stock_history stack
best_stock_history = []
max_dev_hist=[]
history=[]
hist_ind_set=set()
best_stock_tmp=[]
#best_stock_history_tmp=[]
# generates all possibe combinations of the given stocks, bank and magical number
build_magic_graph(start, bank, data, graph, best_stock)

# draw graph
#nx.draw(graph, with_labels=True)
# plt.draw()
# plt.show()

# run djikstra to find the cheapest path to the maximum devidend
# path is the nodes
# length is the total cost of the path
length, path = nx.single_source_dijkstra(graph, 0, max_dev)


#find cheapest combination of the saved best_stock list
cheapest_magic_path,cheapest_magic_path_cost=tools.cheapest_combo(max_dev_hist,stock_rates)

for n in range(0, len(path)-1):
    #    find the stocks that represents the path from djikstra
    ultimate_stock.append(tools.find_cheapest_edge(graph[path[n]][path[n+1]]))

print("Maximum devidend is : %s kr" % max_dev)
print("Total cost magic : %s kr" % cheapest_magic_path_cost)
#print("Magic path : %s" % cheapest_magic_path)

#print("Total cost djikstra : %s kr" % length)
#print("Djikstra path :%s ",ultimate_stock)
#print(path)

#generate the data to excell
tools.gen_data_to_excell(cheapest_magic_path, data, file_location_write)
