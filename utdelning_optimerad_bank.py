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
import sys

def build_graph(start, bank, excell_data, graph, best_stock,best_stock_tmp):
    global max_dev
    global magic_number
    global cheapest_stock
    global best_stock_history
    global best_stock_history_tmp
    global bank_init
    global history
    global max_dev_hist
    global flagsator

    for stock in excell_data.index:
        flagger=False
        dev = 0
        # reset the best_stock when a new path from origin is started
        if start == 0:
            bank=bank_init
            best_stock = []
            best_stock_tmp=[]
#            prev_stock=0
          
        # calc the cost
        cost = stock_rates.iloc[stock].to_numpy()
        # buy the stock
        bank_tmp = bank-cost
        
       # check if you've already have bought the max amount if this stock
        # did you afford it? if not continue to the next stock and try again
        if len(list(filter(lambda i: i['name'] == excell_data.iloc[stock, 0] , best_stock))) < magic_number and bank_tmp >= 0:
#                         
            best_stock.append({'name':excell_data.iloc[stock, 0],'index':stock})
            best_stock=sorted(best_stock, key=lambda i: i['index'])
              
            best_stock_tmp.append({'name':excell_data.iloc[stock, 0],'index':stock,'bank':bank,'bank_tmp':bank_tmp})
            best_stock_tmp=sorted(best_stock_tmp, key=lambda i: i['index'])

#                # if you have made a combination that you've already have done before, continiue to next stock
            for hist in history:
                flag= hist==best_stock
                if flag==True:
                    flagger=flag
                    break
            if flagger==True:
                best_stock=del_first_occurence(best_stock,stock)
                best_stock_tmp=del_first_occurence(best_stock_tmp,stock)
                continue
            
            for month in range(0, len(calendar.columns)):
                # acess the devidend in month for every stock
                dev = dev+calendar.iloc[stock, month]   
            # calculate the total yearly devidend
            dev_tot = np.round(start+dev)
#            print("tmp",best_stock_tmp)
#            print("stock", stock)
#            print(start)

            # save the maximum devidend as a global variable
            if dev_tot >= max_dev:
                flagsator==True
#                    print('inside',dev_tot)
                if dev_tot==max_dev:
                    max_dev_hist.append(list(best_stock))
#                    best_stock_history_tmp.append(list(best_stock_tmp))
                elif dev_tot>max_dev:
                    max_dev_hist=[]
#                    best_stock_history_tmp=[]
                    max_dev_hist.append(list(best_stock))
                    
#                    best_stock_history_tmp.append(list(best_stock_tmp))
                
#                print('dev_hist',max_dev_hist)
#                print("tmp",best_stock_tmp)
                max_dev = dev_tot
            
            # add the bought stock to the stack
            best_stock_history.append(list(best_stock))
            best_stock_history_tmp.append(list(best_stock_tmp))

            history.append(list(best_stock))
            # the key attribute works as name info.
            graph.add_node(dev_tot)
            # add weighted edge from where you were to to stock you just bought
            graph.add_weighted_edges_from(
                [(start, dev_tot, cost)], key=excell_data.iloc[stock, 0])
            
            if bank_tmp >= cheapest_stock:
#                best_stock_local=best_stock
#                best_stock_local_tmp=best_stock_tmp
#                if len(list(filter(lambda i: i['name'] == excell_data.iloc[1, 0] , best_stock)))!=1 and len(list(filter(lambda i: i['name'] == excell_data.iloc[0, 0] , best_stock)))==1 and len(list(filter(lambda i: i['name'] == excell_data.iloc[2, 0] , best_stock)))==1:
#                if flagsator==True:    
#                print('PREV RECK',best_stock_tmp)
                
#                print(stock)
#                    flagsator=True
                # recursively call the function again, start in the just bought stock
                build_graph(dev_tot, bank_tmp, excell_data, graph, best_stock,best_stock_tmp)

##                if len(list(filter(lambda i: i['name'] == excell_data.iloc[1, 0] , best_stock)))!=1 and len(list(filter(lambda i: i['name'] == excell_data.iloc[0, 0] , best_stock)))==1 and len(list(filter(lambda i: i['name'] == excell_data.iloc[2, 0] , best_stock)))==1:
#                if flagsator==True:
#                print('After RECK',best_stock_tmp)
##                    print('After RECK local',best_stock_local_tmp)
#                    tmp=best_stock_history.pop()
#                    print('POOP',tmp)
#                    best_stock_history.append(list(tmp))
#                    print(stock)
#                best_stock=best_stock_local
#                best_stock_tmp=best_stock_local_tmp
            if len(list(filter(None,best_stock)))!=0:
                best_stock=best_stock_history.pop()
                best_stock_tmp=best_stock_history_tmp.pop()
                
#            if len(list(filter(lambda i: i['name'] == excell_data.iloc[1, 0] , best_stock)))!=1 and len(list(filter(lambda i: i['name'] == excell_data.iloc[0, 0] , best_stock)))==1 and len(list(filter(lambda i: i['name'] == excell_data.iloc[2, 0] , best_stock)))==1:
#            if flagsator==True:
#            print('PREV del',best_stock_tmp)
#            print(stock)

#                best_stock = best_stock_history.pop()
#                if len(list(filter(None,best_stock)))>=2:
#                    best_stock=[i for i in best_stock if not (i['index']==stock)]
            
            if len(list(filter(None,best_stock)))!=0:
                #de här tar bort all occurencys and not the first
#                best_stock=[i for i in best_stock if not (i['index']==stock) and flagsator==False]
                
                
                best_stock=del_first_occurence(best_stock,stock)
                best_stock_tmp=del_first_occurence(best_stock_tmp,stock)
          
#                best_stock_tmp=[i for i in best_stock_tmp if not (i['index']==stock)]
                
#            if len(list(filter(lambda i: i['name'] == excell_data.iloc[1, 0] , best_stock)))!=1 and len(list(filter(lambda i: i['name'] == excell_data.iloc[0, 0] , best_stock)))==1 and len(list(filter(lambda i: i['name'] == excell_data.iloc[2, 0] , best_stock)))==1:
#            if flagsator==True:
#            print("AFTER del",best_stock_tmp)
#            print(stock)
        #kolla om det finns ett bra sätt att börja om loopa från början om detta inträffar
#        elif stock == max(excell_data.index) and bank>cheapest_stock:
#            print('knas')
#            flags=True
#            magic_number=magic_number+1
        



def find_cheapest_edge(edge_data):
    # finds the cheapest edge
    # in: 'networkx.classes.coreviews.AtlasView'
    #out: string
    cheapest_stock = math.inf
    for k in edge_data:
        if edge_data[k]['weight'] <= cheapest_stock:
            ultimate_stock = edge_data[k]['key']
    return ultimate_stock


def gen_data_to_excell(stocks, excell_data, file_loc):
    writer = ExcelWriter(file_loc,engine='xlsxwriter')
    for stock in excell_data.index:
        amount=len(list(filter(lambda i: i['name'] == excell_data.iloc[stock, 0] , stocks)))
        df1 = pd.DataFrame({excell_data.iloc[stock, 0]})
        df2 = pd.DataFrame({amount})
        df1.to_excel(writer, 'Result', startcol=0,startrow=stock,header=None, index=False)
        df2.to_excel(writer, 'Result', startcol=1,startrow=stock,header=None, index=False)
    writer.save()

def del_first_occurence(stock_list,index):
    stock_del=[]
    flagsator=False
    for i in stock_list:
        if i['index']==index and flagsator==False:
            flagsator=True
            continue
        stock_del.append(i)
    return stock_del   

flagsator=False
flags=False

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
#bank=4685 borde ge en dev på 178.95 typ
bank = 4000
bank_init=bank
# initialize
magic_number = 1
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
best_stock_tmp=[]
best_stock_history_tmp=[]
# generates all possibe combinations of the given stocks, bank and magical number
build_graph(start, bank, data, graph, best_stock,best_stock_tmp)

# draw graph
#nx.draw(graph, with_labels=True)
# plt.draw()
# plt.show()

# run djikstra to find the cheapest path to the maximum devidend
# path is the nodes
# length is the total cost of the path
length, path = nx.single_source_dijkstra(graph, 0, max_dev)


for n in range(0, len(path)-1):
    #    find the stocks that represents the path
    ultimate_stock.append(find_cheapest_edge(graph[path[n]][path[n+1]]))
    
cheapest_magic_path_cost=math.inf
for combo in max_dev_hist:
    combo_cost=0
    for k in combo:
        combo_cost=combo_cost+stock_rates.iloc[k.get('index')].to_numpy()
    if combo_cost<=cheapest_magic_path_cost:
        cheapest_magic_path_cost=combo_cost
        cheapest_magic_path=combo



print("Maximum devidend is : %s kr" % max_dev)
print("Total cost magic : %s kr" % cheapest_magic_path_cost)
print("Magic path : %s" % cheapest_magic_path)

print("Total cost djikstra : %s kr" % length)
print("Djikstra path :%s ",ultimate_stock)
print(path)

# denna gör inte riktigt det den ska än
gen_data_to_excell(cheapest_magic_path, data, file_location_write)
