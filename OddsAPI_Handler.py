import requests  
import pandas as pd 



API_key = 'b37adb29e40e5387083accb004cf10e1' 


class Bettinglines(): 

    def __init__(self) -> None:
        self.Spreaddic = {'Home_Team': [], 'Home_Price': [], 'Point_Home': [], 'Away_Team': [], 'Away_Price': [], 'Point_Away': [], 'Bookmaker': []} 
        self.MLdic = {'Home_Team': [], 'Home_Price': [], 'Away_Team': [], 'Away_Price': [], 'Bookmaker': []}   
        






    def call_api(self):
        self.response = requests.get(f'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey={API_key}&regions=us&markets=h2h,spreads&oddsFormat=american').json()  
        return self.response
    
    def parse_response(self):  
        response = self.response 
        MLdic = self.MLdic 
        Spreaddic = self.Spreaddic

        for event in response: 

            for bookmaker in event.get('bookmakers', []):
                Spreaddic['Bookmaker'].append(bookmaker.get('title')) 
                MLdic['Bookmaker'].append(bookmaker.get('title'))
                
                for market in bookmaker.get('markets', []):  
                        splitter = (market.get('key'))  
                        if splitter == 'h2h':
                            outcomes = market.get('outcomes', [])
                            MLdic['Home_Team'].append(outcomes[0].get('name'))  
                            MLdic['Home_Price'].append(outcomes[0].get('price'))
                            MLdic['Away_Team'].append(outcomes[1].get('name'))   
                            MLdic['Away_Price'].append(outcomes[1].get('price'))

                                
                            max_len = max(len(v) for v in MLdic.values())


                            for key, value in MLdic.items():
                                while len(value) < max_len:
                                    value.append(None)

                        
                            self.MLdf = pd.DataFrame(MLdic)   
                            
                        
                        else: 
                            outcomes = market.get('outcomes', [])
                            Spreaddic['Home_Team'].append(outcomes[0].get('name'))  
                            Spreaddic['Home_Price'].append(outcomes[0].get('price'))  
                            Spreaddic['Point_Home'].append(outcomes[0].get('point')) 
                            Spreaddic['Away_Team'].append(outcomes[1].get('name'))   
                            Spreaddic['Away_Price'].append(outcomes[1].get('price')) 
                            Spreaddic['Point_Away'].append(outcomes[1].get('point'))  

                            max_len = max(len(v) for v in Spreaddic.values())


                            for key, value in Spreaddic.items():
                                while len(value) < max_len:
                                    value.append(None)

                            self.spreaddf = pd.DataFrame(Spreaddic) 
                        
        
    def to_csv(self): 
        self.MLdf.to_csv('Moneyline.csv', index=False) 
        self.spreaddf.to_csv('Spreads.csv', index=False)
    
    
                        

result = Bettinglines()  
result.call_api() 
result.parse_response() 
result.to_csv()



