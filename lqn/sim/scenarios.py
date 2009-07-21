'''
Created on 18-lug-2009

@author: fabio
'''

from variables import *
from datetime import datetime
from lqn.core.transactions import Transaction, TransactionFailed
#from thelqn import LqnMember

import random

class Scenario(object):
    
    def __init__(self, network):
        self.network    = network  
        self.month_count= 0
    
    def run(self):
        pass


class SimpleScenario(Scenario):
    
    def spend(self,member):
        #for now, just pick a business at random 
        index = random.randint(0,len(self.network.businesses)-1) 
        creditor = self.network.businesses[index]
        credit_account = creditor.get_account()
        #create a ta amount at random
        ta_amount = random.randrange(lower_range_transaction,
                                     upper_range_transaction)
        #timestamp
        tstamp = datetime.now()
        ta = Transaction(credit_account,member.get_account(),
                         ta_amount,tstamp)
        try:
            ta.commit()
            self.network.ta_recorder.add_transaction(ta)
        except TransactionFailed:
            #do nothing for now
            pass
        
        
        
    def __init__(self, network):
        Scenario.__init__(self, network)
    
    def run(self, day):      
            self.day()
                
            if day % 7 == 0 : #this is also end of week
                self.week()
            
            if day % 30 == 0: #this is also end of month
                self.month()    
                
    def day(self):
        #self.network.council_quids.observe(self.network.council.account.get_balance())
        #self.network.a_member_quids.observe(self.network.members[3].account.get_balance())   
        pass
            
    def week(self):
        pass    
            
    def month(self):
        if (self.month_count < quid_injection_business_period):
            self.network.trust.inject(self.network.businesses, increase_step_for_businesses)
                        
        self.month_count += 1