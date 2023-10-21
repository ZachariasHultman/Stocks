
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  18 17:44:14 2020

@author: Zacharias Hultman
"""
import numpy as np
import pandas as pd
from pandas import ExcelWriter
import networkx as nx
#import matplotlib.pyplot as plt
import math
import tools
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk



#GUI code and functions start------------------------------------------------------
def browseReadFiles():
    global filenameRead
    filenameRead=filedialog.askopenfilename(initialdir='/',
                                        title='Select File',
                                        filetypes=(('Excel files','*.xlsx*'),('all files',
                                                     '*.*')))
    label_file_explorer2.configure(text='File Opened: ' +filenameRead)
#    return filenameRead
    
def browseSaveFiles():
    global filenameSave
    filenameSave=filedialog.askopenfilename(initialdir='/',
                                        title='Select File',
                                        filetypes=(('Excel files','*.xlsx*'),('all files',
                                                     '*.*')))
    label_file_explorer2.configure(text='File to Save Results at: ' +filenameSave)
#    return filenameSave
    
def close_window():
    window.destroy()


window=tk.Tk()
    
window.title('Magic Super Program')

window.geometry('320x250')

window.config(background='white')

label_file_explorer1=tk.Label(window,
                          text='Get Rich!',
                          width=20, height=4,
                          fg='blue')
label_file_explorer1.grid(row=0,column=0)
label_file_explorer2=tk.Label(window,
                          text='Choose a file',
                          width=20, height=4,
                          fg='blue')
label_file_explorer2.grid(row=0,column=1)

button_explore=tk.Button(window,
                      text='Choose read file',
                      command= browseReadFiles)
button_explore.grid(row=2,column=1)

button_save=tk.Button(window,
                      text='Choose save file',
                      command= browseSaveFiles)
button_save.grid(row=3,column=1)

magic_label=tk.Label(window,
                  text='Magic Number',
                  font=('calibre',10,'bold'))
                  
magic_label.grid(row=4,column=0)

magic_text=tk.IntVar()
magic_Entry=tk.Entry(window,
                 textvariable = magic_text,
                font=('calibre',10,'bold'))

magic_Entry.grid(row=4,column=1)

bank_label=tk.Label(window,
                  text='Bank',
                  font=('calibre',10,'bold'))
bank_label.grid(row=5,column=0)

bank_text=tk.IntVar()
bank_Entry=tk.Entry(window,
                 textvariable = bank_text,
                font=('calibre',10,'bold'))

bank_Entry.grid(row=5,column=1)

sheet_label=tk.Label(window,
                  text='Sheet Name in Read File',
                  font=('calibre',10,'bold'))
sheet_label.grid(row=6,column=0)

sheet_Name=tk.StringVar()
sheet_Entry=tk.Entry(window,
                 textvariable = sheet_Name,
                font=('calibre',10,'bold'))

sheet_Entry.grid(row=6,column=1)



button_exit=tk.Button(window,
                      text='Run!',
                      command= close_window)
button_exit.grid(row=8,column=1)

window.mainloop()

#GUI code and functions ends------------------------------------------------------

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
#            magic_number=magic_number_init
        # calc the cost
        cost = stock_rates.iloc[stock].to_numpy()
        # buy the stock
        bank_tmp = bank-cost
       # check if you've already have bought the max amount if this stock
        # did you afford it? if not continue to the next stock and try again
        if len(list(filter(lambda i: i['name'] == excell_data.iloc[stock, 0] , best_stock))) < magic_number and bank_tmp >= 0:          
            best_stock.append({'name':excell_data.iloc[stock, 0],'index':stock})
            best_stock=sorted(best_stock, key=lambda i: i['index'])
            hist_ind=0
            counter=0
            for b in best_stock:
                counter=counter+1
                hist_ind=hist_ind+(100**(counter))*b.get('index')
            if hist_ind in hist_ind_set:
                best_stock=tools.del_first_occurence(best_stock,stock)
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
        elif stock == max(excell_data.index) and bank>cheapest_stock and len(list(filter(None,best_stock)))==total_amount_stocks*magic_number:
            magic_number=magic_number+1
            print('Increase magic number. New magic:' , magic_number)
            build_magic_graph(start, bank, excell_data, graph, best_stock)
            magic_number=magic_number-1
            print('Decrease magic number. New magic:' , magic_number)


sheet=sheet_Name.get()
file_location = filenameRead
file_location_write = filenameSave

data = pd.read_excel(file_location,
                     sheet_name=sheet, keep_default_na=False)
cols = range(1, 13)
calendar = pd.read_excel(file_location,
                         sheet_name=sheet, usecols=cols, keep_default_na=False)
stock_rates = pd.read_excel(file_location,
                            sheet_name=sheet, usecols=[15], keep_default_na=False)
print(data)


magic_number_init=magic_text.get()

data_write = pd.read_excel(file_location_write,
                           sheet_name='Result', keep_default_na=False)
# The amount of money i have to buy for
bank_init=bank_text.get()
bank=bank_init
# initialize
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

## draw graph
#nx.draw(graph, with_labels=True)
#plt.draw()
#plt.show()



#find cheapest combination of the saved best_stock list
cheapest_magic_path,cheapest_magic_path_cost=tools.cheapest_combo(max_dev_hist,stock_rates)


print("Maximum devidend is : %s kr" % max_dev)
print("Total cost magic : %s kr" % cheapest_magic_path_cost)
#print("Magic path : %s" % cheapest_magic_path)



#generate the data to excell
tools.gen_data_to_excell(cheapest_magic_path, data, max_dev, file_location_write)

#input('Press enter to exit')
