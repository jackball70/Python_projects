import pandas as pd 
import numpy as np 
from datetime import datetime as dt, timedelta 
import matplotlib.pyplot as plt   
import yfinance as yf

today = dt.today()
weeksback = today - timedelta(days=365) 
startdate = today.strftime('%Y-%m-%d') 
enddate = weeksback.strftime('%Y-%m-%d') 
intial_portfolio_value = 10000


class monteCarlo_Stock_Analysis: 

    def get_stock_data(self):  
        EV_Stock_list = ['LI','LCID', 'F', 'GM', 'RIVN', 'TSLA', 'NIO'] 
        stock_data = yf.download(EV_Stock_list, start= enddate, end = startdate, progress= False) 
        stock_data = stock_data[[ "Close"]]    
        returns = stock_data.pct_change() 
        self.meanreturns = returns.mean() 
        self.covmatrix = returns.cov() 
        return self.meanreturns, self.covmatrix  
    
    def monte_model_vis(self): 
        weights = np.random.random(len(self.meanreturns)) 
        weights /= np.sum(weights) 
        MC_simulations = 100   
        timeframe_in_days =  100  
        meanm = np.full(shape=(timeframe_in_days, len(weights)), fill_value= self.meanreturns) 
        meanm = meanm.T 
        portfolio_sims = np.full(shape=(timeframe_in_days, MC_simulations), fill_value= 0.0)
        
        for simulations in range(0, MC_simulations):  
            Z = np.random.normal(size=(timeframe_in_days, len(weights))) 
            L = np.linalg.cholesky(self.covmatrix) 
            dailyreturns = meanm + np.inner(L, Z) 
            portfolio_sims[:,simulations] = np.cumprod(np.inner(weights, dailyreturns.T)+1)*intial_portfolio_value 

        plt.plot(portfolio_sims) 
        plt.ylabel('Portfolio Value ($)') 
        plt.xlabel('Days') 
        plt.title('EV portfolio Monte Carlo simulation') 
        plt.show()



    


result = monteCarlo_Stock_Analysis() 
result.get_stock_data() 
result.monte_model_vis()