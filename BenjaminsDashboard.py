import requests 
import pandas as pd  
import yfinance as yf 
import plotly.graph_objects as go
import plotly.express as px
from datetime import timedelta, datetime 
#import pandas_datareader.data as web
import json  



base_url = 'https://www.alphavantage.co/query?function' 
API_KEY = 'BSSWWN36D4EIIU4B' 
today = datetime.today()
weeksback = today - timedelta(days=365) 
startdate = today.strftime('%Y-%m-%d') 
enddate = weeksback.strftime('%Y-%m-%d')

class Bens_Dashboard:  
    
    def __init__(self): 
        self.dates = [] 
        self.data = []

    def sp_vis(self):   
        data = yf.download('^GSPC',start= enddate, end= startdate, progress=False)
        data["Date"] = data.index
        data = data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
        data.reset_index(drop=True, inplace=True)
        figure = go.Figure(data=[go.Candlestick(x=data["Date"],
        open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"])])
        figure.update_layout(title = "S&P500 Price Analysis", xaxis_rangeslider_visible=False)
        figure.show()   

    def vis_of_gold(self): 
        data = yf.download('GC=F',start= enddate, end= startdate, progress=False)
        data["Date"] = data.index
        data = data[["Date", "Open", "High", "Low",
                    "Close", "Adj Close", "Volume"]]
        data.reset_index(drop=True, inplace=True)
        figure = go.Figure(data=[go.Candlestick(x=data["Date"],
        open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"])])
        figure.update_layout(title = "Gold Price Analysis", xaxis_rangeslider_visible=False)
        figure.show()
        

    def get_forex_data(self):  
        from_currency = input('Ben, Please enter your from currency, example JPY:') 
        to_currency = input('Ben, Please enter your to currency:') 
        from_currency.upper() 
        to_currency.upper()
        response = requests.get(f'{base_url}=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}')  
        forexdata = response.json() 
        print(forexdata)
        
        
    
  
        
       



result = Bens_Dashboard()  
result.sp_vis()
result.vis_of_gold() 
result.get_forex_data()
