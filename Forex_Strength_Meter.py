   
import freecurrencyapi 
import matplotlib.pyplot as plt 


base_url = 'https://api.freecurrencyapi.com/v1/latest'
API_key = 'fca_live_ZDMaVj4KECBHeoSh6hHfiHht5mJk7URK65PsaWuS'  
client = freecurrencyapi.Client(API_key)
  

base_pairs = ['AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD']  
targets =  ['AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD']  

AUD = [] 
CAD = [] 
CHF = [] 
EUR = [] 
GBP = [] 
JPY = [] 
NZD = [] 
USD = [] 

for base in base_pairs: 
    response = client.latest(base_currency=base, currencies=targets)   
    
    for key in targets:
        if base == 'AUD':   
            AUD.append(1 / response['data'][key])  
            AUDstrength = sum(AUD) / len(targets)  
        elif base == 'CAD':   
            CAD.append(1 / response['data'][key]) 
            CADstrength = sum(CAD) / len(targets)
        elif base == 'CHF':  
            CHF.append(1 / response['data'][key])  
            CHFstrength = sum(CHF) / len(targets)
        elif base == 'EUR':  
            EUR.append(1 / response['data'][key])  
            EURstrength = sum(EUR) / len(targets)
        elif base == 'GBP':  
            GBP.append(1 / response['data'][key])  
            GBPstrength = sum(GBP) / len(targets)
        elif base == 'JPY':  
            JPY.append(1 / response['data'][key])  
            JPYstrength = sum(JPY) / len(targets)
        elif base == 'NZD':  
            NZD.append(1 / response['data'][key])  
            NZDstrength = sum(NZD) / len(targets)
        else: 
            USD.append(1 / response['data'][key])   
            USDstrength = sum(USD) / len(targets)
   
data = {'AUD': AUDstrength, 'CAD': CADstrength, 'CHF': CHFstrength, 'EUR': EURstrength,  
        'GBP': GBPstrength, 'JPY': JPYstrength, 'NZD': NZDstrength, 'USD': USDstrength} 
country = list(data.keys()) 
values = list(data.values()) 

fig = plt.figure(figsize= (10, 5)) 
plt.bar(country, values, color='green', width=0.4)  
plt.xlabel("CURRENCY") 
plt.ylabel("CURRENCY STRENGTH") 
plt.title("Forex Strength Chart") 
plt.show()