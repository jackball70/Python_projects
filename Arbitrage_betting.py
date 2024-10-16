import pandas as pd 
import numpy as np 


class ArbitrageBetting: 

    def __init__(self) -> None:
        self.MLdf = pd.read_csv('Moneyline.csv') 
        self.Spreaddf = pd.read_csv('Spreads.csv') 
        # n is the bet ammount  
    def format_ML_data(self): 
       mldf = self.MLdf 
       mldf['Home_Price'] = mldf['Home_Price'].apply(lambda x: (1 + x/100) if x > 0 else (1 + 100/x))  
       mldf['Away_Price'] = mldf['Away_Price'].apply(lambda x: (1 + x/100) if x > 0 else (1 + 100/x))   
       gamegroups = mldf.groupby(['Home_Team', 'Away_Team']).filter(lambda x: len(x) >= 10) 
       gamegroups = gamegroups.groupby(['Home_Team', 'Away_Team']).max(['Home_price', 'Away_price'])  
       self.gamegroups = gamegroups
       return self.gamegroups 
    def Identifying_ML_Arbitrage_opps(self): 
        gamesdf = self.gamegroups 
        gamesdf['Arbigtrage_Ability'] = 1 / gamesdf['Home_Price'] + 1 / gamesdf['Away_Price']  
        print(gamesdf.head(12))


    def format_spread_data(self): 
        spreaddf = self.Spreaddf 
        spreaddf['Home_Price'] = spreaddf['Home_Price'].apply(lambda x: (1 + x/100) if x > 0 else (1 + 100/x))  
        spreaddf['Away_Price'] = spreaddf['Away_Price'].apply(lambda x: (1 + x/100) if x > 0 else (1 + 100/x))   
        spreadgamegroups = spreaddf.groupby(['Home_Team', 'Away_Team', 'Point_Home', 'Point_Away']).filter(lambda x: len(x) >= 10)   
        spreadgamegroups = spreadgamegroups.groupby(['Home_Team', 'Away_Team', 'Point_Home', 'Point_Away']).max(['Home_price', 'Away_price'])
        self.spreadgamegroups = spreadgamegroups 
        return self.spreadgamegroups 
    def Identifying_Spread_Arbitrage_opps(self): 
        spreadarb = self.spreadgamegroups
        spreadarb['Arbigtrage_Ability'] = 1 / spreadarb['Home_Price'] + 1 / spreadarb['Away_Price']  
        print(spreadarb.head(12))
    

       
    
    

result = ArbitrageBetting()
result.format_ML_data() 
result.Identifying_ML_Arbitrage_opps() 
result.format_spread_data()