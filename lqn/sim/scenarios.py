'''
Created on 18-lug-2009

@author: fabio
'''
from lqn.sim import logger

from variables import *
from datetime import datetime
from lqn.core.transactions import Transaction, TransactionFailed
from lqn.core.policy import TransactionDataAccessor
from lqn.core.policy import SimplePolicy

from activity import TransactionRecorder

import random

class Scenario(object):
    
    def __init__(self, network):
        self.network        = network  
        self.month_count    = 0
        self.data_accessor  = TransactionRecorderDataAccessor(network.ta_recorder)
        self.initial_policy = SimplePolicy()
        self.current_policy = self.initial_policy
    
    def run(self):
        pass


class SimpleScenario(Scenario):
    '''
    In the SimpleScenario, these are the current assumptions:
    
    - Every ordinary member makes a random trade between per day 10Q and 100Q
         and waits 1 day
    - Council employees make 3 random trades between 10Q and 100Q and 
        wait at random between 1 and 3 days
    - Every business member makes a random trade between 100Q and 1000Q,
        three minor trades between 10Q and 100Q, and waits 3 days
    - The council spends only once a month 10% of wages to its employees,
        averaged at 400Q
    '''
    
    def spend(self,member):        
        member_type = member.__class__.__name__
        logger.debug("Class name: %s", member_type)
        
        ta_amount = 0
        wait_time = 1.0
        
        if (member_type == "LqnMember"):
            #for now, just pick a business at random
            self.trade(member)
            
        elif (member_type == "LqnEmployee"):
            for i in range(0,4):
                self.trade(member)
            wait_time = random.randrange(1.0,3.0)
            wait_time = float(wait_time)
            
        elif (member_type == "LqnTrust"):
            pass
        elif (member_type == "LqnBusiness"):
            range_factor = 10
            for i in range(0,4):
                self.trade(member, range_factor)
            wait_time = 3.0
        else:
            pass
                
        
        return wait_time
        
    def trade(self, member, range_factor = 1):
        index = random.randint(0,len(self.network.businesses)-1) 
        creditor = self.network.businesses[index]
        credit_account = creditor.get_account()
        #create a ta amount at random
        ta_amount = random.randrange(lower_range_transaction*range_factor,
                                     upper_range_transaction*range_factor)
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
            self.day(day)
                
            if day % 7 == 0 : #this is also end of week
                self.week(day)
            
            if day % 30 == 0: #this is also end of month
                self.month(day)    
                
    def day(self, day):
        #self.network.council_quids.observe(self.network.council.account.get_balance())
        #self.network.a_member_quids.observe(self.network.members[3].account.get_balance())
        if ( (day >0) and (day % policy_application_period == 0) ):
            self.current_policy.observation_start = day - 7
            self.current_policy.observation_end = day
            self.network.trust.apply_policy(self.data_accessor,
                                            self.network.all_members,
                                            self.current_policy )
            
    def week(self, day):
        pass    
            
    def month(self, day):
        logger.info("Simulation now runs in month: %d", self.month_count)
        if (self.month_count < quid_injection_business_period):
            logger.info("Still in initial quids injection period for businesses --> Quids will be injected to businesses.")
            self.network.trust.inject(self.network.businesses, increase_step_for_businesses)
                        
        self.month_count += 1
        

class TransactionRecorderDataAccessor(TransactionDataAccessor):
    
    def __init__(self, ta_recorder):
        self.ta_recorder = ta_recorder
    
    def get_transactions_in_period(self,start,end,account):
        self.ta_recorder.get_transactions(start, end, account)