import time
import pandas as pd 
import yfinance as yf  
import streamlit as st
from prophet import Prophet as pr 


st.title("Interactive stock Predictor using Facebooks Prophet Model")  
 
userinput = st.text_input("Please enter a ticker to be predicted:")   
ticker = yf.Ticker(userinput)  
ticker = ticker.history(period='max')   
stockdf = pd.DataFrame(ticker) 


stockdf = stockdf.drop(['Dividends','Stock Splits', 'Open', 'High', 'Low', 'Volume'], axis=1)  
stockdf['Date'] = stockdf.index 
stockdf['Date'] = stockdf['Date'].apply(lambda x: str(x)[:11]) 
stockdf['Date'] = pd.DatetimeIndex(stockdf['Date']) 
formatted_df = stockdf.rename(columns={'Date': 'ds', 'Close': 'y'}) 





"""Calling Prophet model for our users selected stock ticker. 
The data has been formatted to have just the column we are trying to predict which is close price and the date of following close 
prices. It will also visualize the data into a couple diffrent plots""" 
pm = pr(interval_width=0.95)  
model = pm.fit(formatted_df) 
future = pm.make_future_dataframe(periods=365, freq='D') 
forecast = pm.predict(future)   
if st.checkbox('Show dataframe'):  
    st.write(forecast) 
plot1 = pm.plot(forecast) 
plot2 = pm.plot_components(forecast) 
st.plotly_chart(plot1) 
if st.checkbox("Show More in depth Charts"):
    st.plotly_chart(plot2)

 



    """def format_data(stockdf): 
        This function below formats the data to be used int he prophet model. I start with dropping all the columns that are not needed 
        Becuase the prophet model only needs a date and a predicted value column which is labeled as y. The dtae had to be correctly formatted 
        using the lambda functionality to turn the date column into a string and take the first 10 charachters of the string. 
        stockdf = stockdf.drop(['Dividends','Stock Splits', 'Open', 'High', 'Low', 'Volume'], axis=1)  
        stockdf['Date'] = stockdf.index 
        stockdf['Date'] = stockdf['Date'].apply(lambda x: str(x)[:11]) 
        stockdf['Date'] = pd.DatetimeIndex(stockdf['Date']) 
        formatted_df = stockdf.rename(columns={'Date': 'ds', 'Close': 'y'})  
        print(formatted_df.dtypes) 
        print(formatted_df.head())  
        Prophet_model_Activator(formatted_df) 



    def Prophet_model_Activator(formatted_df): 
        Calling Prophet model for our users selected stock ticker. 
            The data has been formatted to have just the column we are trying to predict which is close price and the date of following close 
            prices. It will also visualize the data into a couple diffrent plots
        pm = pr(interval_width=0.95)  
        model = pm.fit(formatted_df) 
        future = pm.make_future_dataframe(periods=365, freq='D') 
        forecast = pm.predict(future) 
        print(forecast.tail())  
        plot1 = pm.plot(forecast) 
        plot2 = pm.plot_components(forecast)
        plot1.show() 
        plot2.show()  
        
      try
            userinput = st.text_input("Please enter a ticker to be predicted:")   
        ticker = yf.Ticker(userinput)  
        ticker = ticker.history(period='max')   
        stockdf = pd.DataFrame(ticker) 
    except Exception:  
        st.write("Pleae enter a Valid Stock Ticker") 
        continue """