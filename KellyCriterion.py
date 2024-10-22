import pandas as pd 
import numpy as np 

#formula for probality with sports bets (1 + x/100) if x > 0 else (1 + 100/x) 
'''x = int(input("Please Enter your odds for outcome you want:"))   
x2 = int(input("Please Enter your odds for the opposite outcome:"))  
n = int(input("Please Enter the amount your are gambling:"))'''   


class kellycriterionsportsbetting():    
    
    Kelly_Multiplier = 0.5 

    def __init__(self, x, x2, n) -> None: 
        self.x = x 
        self.x2 = x2 
        self.n = n 
        self.payout = 0 
        self.fairwinprob = 0
        self.ev = 0
        # kelly multiplier k =  
    
    def unbaking_vig(self):
        probwinwithvig =  (100 /(self.x + 100)) if self.x > 0  else (abs(self.x) /(abs(self.x) + 100))  
        problosswithvig = (100 /(self.x2 + 100)) if self.x2 > 0  else (abs(self.x2) /(abs(self.x2) + 100))  
        self.fairwinprob = probwinwithvig / (problosswithvig + probwinwithvig) 
        print(self.fairwinprob)
    def calculating_payout(self):
        if self.x > 0 :
            self.payout +=  (self.x/100) * self.n 

        else:  
            self.payout += (100 / abs(self.x)) * self.n
        
        return self.payout, print(self.payout) 
    
    def expected_value(self):
        lossprob = 1 - self.fairwinprob 
        w = self.fairwinprob * self.payout
        l = self.n * lossprob 
        self.ev += w - l    
        print(self.ev)
        if self.ev > 0: 
            print(f"profit strategy is possible, estimated value is {self.ev}")  
            return self.ev  
        else: 
            print("These odds do not have a possible profit strategy!\n Please supply other odds or play at your own risk")   
            return 0 
        
    def Kelly_criterion(self):  
        unitstobet = (100 * self.Kelly_Multiplier) * (self.ev/self.payout) 
        print(f'Please bet {unitstobet} units') 
        return unitstobet

result = kellycriterionsportsbetting(-170, 160, 12) 
result.unbaking_vig()  
result.calculating_payout() 
result.expected_value() 
result.Kelly_criterion()