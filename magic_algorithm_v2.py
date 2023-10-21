
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  18 17:44:14 2020

@author: Zacharias Hultman
"""
import numpy as np
import pandas as pd
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

def build_magic_graph(data,bank, magic_number):

    df=data[["Aktie"]]
    col_list=list(data.iloc[:,1:13])

    df["Yearly dividend"]=data.loc[:,col_list].sum(axis=1,numeric_only=True)
    df["Previous close"]=data[["Previous close"]]
    df["Magic value"]=df["Yearly dividend"]/df["Previous close"]
    df.sort_values(by="Magic value",ascending=False,inplace=True)
    df["Amount"]=0
    df.reset_index(inplace=True,drop=True)
    while bank >= df["Previous close"].min():
        for m_ind in df.index:
            price=df.iloc[m_ind]["Previous close"]
            while bank - price > 0 and df.iloc[m_ind]["Amount"] < magic_number:
                bank-=price
                df.at[m_ind,"Amount"]+=1
        magic_number+=1

    dividend=0
    for ind in df.index:
        dividend+=df.at[ind,"Yearly dividend"]*df.at[ind,"Amount"]

    df["Total yearly dividend"]=dividend
    return df

sheet=sheet_Name.get()
file_location = filenameRead
file_location_write = filenameSave

data = pd.read_excel(file_location,
                     sheet_name=sheet, keep_default_na=False)
magic_number_init=magic_text.get()

# The amount of money i have to buy for
bank_init=bank_text.get()
bank=bank_init
# initialize
magic_number = magic_number_init
# generates all possibe combinations of the given stocks, bank and magical number
magic_df=build_magic_graph(data, bank ,magic_number)
magic_df.drop(["Magic value", "Previous close","Yearly dividend"],axis=1,inplace=True)
magic_df.to_excel(file_location_write)

