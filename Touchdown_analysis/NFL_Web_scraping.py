import numpy as np 
import pandas as pd 
import random 
import time 

class PFR_web_scraping:

    def __init__(self):
        self.seasons = [str(season) for season in range(2014, 2024)] 
        self.teams = ['crd', 'atl', 'rav', 'buf', 'car', 'chi', 'cin', 'cle', 'det', 'dal', 'den', 'htx', 'gnb', 
         'clt', 'jax', 'kan', 'sdg', 'ram', 'rai', 'mia', 'min', 'nwe', 'nor', 'nyg', 'nyj', 'phi', 'pit', 'sea', 'sfo', 'tam', 'oti', 'was'] 


    def season_scrape(self):  
        seasons = self.seasons  
        teams = self.teams 
        nfl_df = pd.DataFrame() 

        for season in seasons: 

            for team in teams: 

                url = 'https://www.pro-football-reference.com/teams/' + team + '/' + season + '/gamelog/'    

                off_df = pd.read_html(url, header=1, attrs={'id': 'gamelog' + season})[0] 

                def_df = pd.read_html(url, header=1, attrs={'id': 'gamelog_opp' + season})[0] 

                teamdf = pd.concat([off_df, def_df], axis = 1) 
                teamdf.insert(loc=0, column='Season', value=season)  
                teamdf.insert(loc=2, column='Team', value=team.upper()) 
                
                time.sleep(random.randint(4,5)) 

                nfl_df = pd.concat([nfl_df, teamdf], ignore_index=True)  

                time.sleep(random.randint(4,5))  

        return nfl_df.to_csv('nfl_gamelogs_2014-2023.csv', index = False)   
 

    def clean_nfl_df(self):   
        nfl_df = pd.read_csv('nfl_gamelogs_2014-2023.csv')
        nfl_pts_df = nfl_df.drop(nfl_df.columns[12:], axis=1) 
        nfl_pts_df = nfl_pts_df.drop(nfl_pts_df.columns[5:6], axis = 1)  
        column_names = {'Unnamed: 4': 'Win', 'Unnamed: 6': 'Home', 'Tm':'Off_Pts', 'Opp.1':'Def_Pts'} 
        nfl_pts_df = nfl_pts_df.rename(columns=column_names)   
        team_dict = {'Arizona Cardinals': 'CRD', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'RAV', 
                     'Buffalo Bills': 'BUF', 'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI', 'Cincinnati Bengals': 'CIN', 
                     'Cleveland Browns': 'CLE', 'Dallas Cowboys': 'DAL', 'Denver Broncos': 'DEN', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GNB', 
                     'Houston Texans': 'HTX', 'Indianapolis Colts': 'CLT', 'Jacksonville Jaguars': 'JAX', 'Kansas City Chiefs': 'KAN', 'Los Angeles Chargers': 'SDG', 
                     'Los Angeles Rams': 'RAM', 'Las Vegas Raiders': 'RAI', 'Oakland Raiders': 'RAI', 'Miami Dolphins': 'MIA', 'Minnesota Vikings': 'MIN', 
                     'New England Patriots': 'NWE', 'New Orleans Saints': 'NOR', 'New York Giants': 'NYG', 'New York Jets': 'NYJ', 'Philadelphia Eagles': 'PHI', 
                     'Pittsburgh Steelers': 'PIT', 'St. Louis Rams': 'RAM', 'San Diego Chargers': 'SDG', 'San Francisco 49ers': 'SFO', 'Seatlle Seahawks': 'SEA', 
                     'Tampa Bay Buccaneers': 'TAM', 'Tennessee Titans': 'OTI', 'Washingtpn Commanders': 'WAS', 'Washington Football Team': 'WAS', 
                     'Washington Redskins': 'WAS'}  
        nfl_pts_df = nfl_pts_df.replace({'Opp': team_dict})  
        nfl_pts_df['Win'] = nfl_pts_df['Win'].apply(lambda x: 1 if x == 'W' else 0) 
        nfl_pts_df['Home'] = nfl_pts_df['Home'].apply(lambda x: 0 if x == '@' else 1) 
        nfl_pts_df = nfl_pts_df.drop('OT', axis=1)   
        self.nfl_pts_df = nfl_pts_df 
        return self.nfl_pts_df 

    def Vegas_lines_scrape(self):  
        seasons = self.seasons  
        teams = self.teams 
        Vegas_df = pd.DataFrame() 

        for season in seasons: 

            for team in teams: 

                url = 'https://www.pro-football-reference.com/teams/' + team + '/' + season + '_lines.htm'    

                lines_df = pd.read_html(url, header=0, attrs={'id': 'vegas_lines'})[0]  

                lines_df.insert(loc=0, column='Season', value=season) 
                lines_df.insert(loc=2, column='Team', value=team.upper()) 

                Vegas_df = pd.concat([Vegas_df, lines_df], ignore_index=True) 
                
                time.sleep(random.randint(4,5)) 

                 

        return Vegas_df.to_csv('nfl_Vegas_lines_2014-2023.csv', index = False)    
    
    def clean_Vegas_df(self):  
        vegas_df = pd.read_csv('nfl_Vegas_lines_2014-2023.csv')  
        print(vegas_df.head())
        vegas_df = vegas_df.drop(vegas_df.columns[6:], axis=1)
        column_names = {'G#': 'G', 'Over/Under':'Total'} 
        vegas_df = vegas_df.rename(columns=column_names)  

        vegas_df = vegas_df.query('(Season <= 2020 and G < 17) or (Season >= 2021 and G < 18)')
        
        vegas_df['Home'] = vegas_df['Opp'].apply(lambda x: 0 if x[0] == '@' else 1) 
        vegas_df['Opp'] = vegas_df.loc['Opp'].apply(lambda x: x[1:] if x[0] == '@' else x) 

        abbr_dict = {'OAK': 'RAI', 'LVR': 'RAI', 'STL': 'RAM', 
                    'LAR': 'RAM', 'LAC': 'SDG', 'IND': 'CLT', 'HOU': 'HTX', 'BAL': 'RAV', 'ARI': 'CRD', 'TEN': 'OTI'} 
        vegas_df = vegas_df.replace({'Opp': abbr_dict}) 
        self.vegas_df = vegas_df 

        return self.vegas_df
 
    
    def merge_df(self): 
       nfl_pts_df = self.clean_nfl_df()  
       Vegas_df = self.clean_Vegas_df() 

       merge_df = pd.merge(nfl_pts_df, Vegas_df, on=['Season', 'Team', 'Opp', 'Home']) 
       merge_df.to_csv('nfl_pts_and_vegas_2014-2023.csv', index=False) 

         






               


result = PFR_web_scraping()  

#result.season_scrape() 
#result.clean_nfl_df() 
#result.Vegas_lines_scrape() 
#result.clean_Vegas_df() 
result.merge_df()
