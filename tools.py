# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:39:29 2020

@author: Zacharias Hultman
"""

import math
import numpy as np
import pandas as pd
from pandas import ExcelWriter
import networkx as nx
   
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

def cheapest_combo(max_dev_hist,stock_rates):
    cheapest_magic_path_cost=math.inf
    for combo in max_dev_hist:
        combo_cost=0
        for k in combo:
            combo_cost=combo_cost+stock_rates.iloc[k.get('index')].to_numpy()
        if combo_cost<=cheapest_magic_path_cost:
            cheapest_magic_path_cost=combo_cost
            cheapest_magic_path=combo
    return cheapest_magic_path,cheapest_magic_path_cost

