import numpy as np 
from   scipy.stats import norm

r = 0.01 
s = 30 
k = 40 
t = 240/365 
sigma = 0.30 

def blackscholes(r, s, k, t, sigma, type='C'): 
    d1 = (np.log(s/k) + (r + sigma**2/2)*t)/(sigma*np.sqrt(t)) 
    d2 = d1 - sigma*np.sqrt(t) 
    try: 
        if type == "C": 
            price = s*norm.cdf(d1, 0, 1) - k*np.exp(-r*t)*norm.cdf(d2, 0, 1) 
        elif type == "p": 
            price = k*np.exp(-r*t)*norm.cdf(-d2, 0, 1) - s*norm.cdf(-d1, 0, 1) 
        return price  
    except: 
        print("Confirm all option parameters above") 


print("option price is: ", round(blackscholes(r, s, k, t, sigma, type='C'), 2))
