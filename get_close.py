import numpy as np
import pandas as pd
import yfinance as yf
from currency_converter import CurrencyConverter

API_KEY="61YTUPZQCTNE374L"

path="/home/zacharias/Documents/Stocks/Aktie_Utdelning.xlsx"

writer=pd.ExcelWriter(path,engine='openpyxl',mode='a',if_sheet_exists='replace')
data = pd.read_excel(path,sheet_name="Python", keep_default_na=False,engine='openpyxl')

res = pd.DataFrame()

c = CurrencyConverter()

for ticker in data['Aktie']:
    
    print(ticker)
    ticker=ticker.split('(')[-1].split(')')[0]
    exchange=ticker.split(':')[0]
    ticker_name=ticker.split(':')[-1]
    if exchange == 'XSTO':        
        if len(ticker_name.split(' ')) != 1:
            ticker_name=ticker_name.replace(' ','-')
        ticker_name=ticker_name+".ST"
        prev_close=yf.Ticker(ticker_name).info['previousClose']
    elif exchange == 'XNYS':
        prev_close=yf.Ticker(ticker_name).info['previousClose']
        prev_close=round(c.convert(prev_close,'USD','SEK'))

    df=pd.DataFrame({'Aktie':[ticker],'Price':[prev_close]})
    res=pd.concat([res,df],ignore_index=True,axis=0)



res.to_excel(writer,'get_close')
writer.save()
writer.close
