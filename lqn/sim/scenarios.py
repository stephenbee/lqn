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
        self.data_accessor  = TransactionRecorderDataAccessor(
                                        network.ta_recorder)
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
        '''
        Called from the LqnMember's individual PEM method!
        '''        
        member_type = member.__class__.__name__
        logger.debug("Class name: %s", member_type)
        
        #ta_amount = 0
        wait_time = 1.0
        #depending on the account type, different behaviour
        if (member_type == "LqnMember"):
            #for now, just pick a business at random
            self.trade(member)
            
        elif (member_type == "LqnEmployee"):
            for i in range(0,4):
                self.trade(member)
            wait_time = random.randrange(1.0,3.0)
            wait_time = float(wait_time)
        elif (member_type == "LqnCouncil"):
            #TODO: What does the council do?
            pass
        elif (member_type == "LqnTrust"):
            #The trust should probably never trade itself,
            #it "only" manages quid supply through quid injection/extraction 
            pass
        elif (member_type == "LqnBusiness"):
            range_factor = 2#10
            for i in range(0,4):
                self.trade(member, range_factor)
            wait_time = 3.0
        else:
            pass
        return wait_time
    
        
    def trade(self, member, range_factor = 1):
        '''
        When the individual LqnMember PEM triggers "spend",
        depending on the algorithm, at some point everybody does a trade.
        So a trade is a transaction of a certain amount, with a 
        debit and a credit account. 
        '''
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
        '''
        This is an event type of method. So on every tick (read day),
        the network triggers the scenario's run (this) method,
        where bookkeeping and account management can happen.
        '''      
        self.day(day)     #run stuff do be done every day
            
        if day % 7 == 0 : #this is also end of week
            self.week(day)
        
        if day % 30 == 0: #this is also end of month
            self.month(day)    
                
    def day(self, day):
        #self.network.council_quids.observe(self.network.council.account.get_balance())
        #self.network.a_member_quids.observe(self.network.members[3].account.get_balance())
        
        #check if it's time to apply the policy. Currently we apply every week,
        #so instead of this check we could put this code into the week() method.
        #However, it might be decided that the period is some arbitrary number
        #of days, so we need to check this.
        if ( (day > no_policy_period) and (day % policy_application_period == 0) ):
            self.current_policy.observation_start = day - 7
            self.current_policy.observation_end = day
            self.network.trust.apply_policy(self.data_accessor,
                                            self.network.all_members,
                                            self.current_policy )
        #In order to calculate daily balances, record them on a per account basis.
        self.network.record_daily_balances()
        
    def week(self, day):
        pass    
            
    def month(self, day):
        logger.info("Simulation now runs in month: %d", self.month_count)
        #The current scenario implies that for an initial period, businesses
        #get some quids injected for an initial period, after which no injectio
        #takes place anymore
        if (self.month_count < quid_injection_business_period):
            logger.info("Still in initial quids injection period for businesses --> Quids will be injected to businesses.")
            self.network.trust.inject(self.network.businesses, increase_step_for_businesses)
        #at the end of the month, the council pays its employees, partly in quids
        self.network.council.pay_employees(self.network.employees);              
        #increase month count
        self.month_count += 1
        

class TransactionRecorderDataAccessor(TransactionDataAccessor):
    '''
        In the simulation we don't have a database, everything is stored
        in memory. To access data, instead of SQL statements, we access
        objects in memory, the TransactionDataAccessor in lqn.core.policy
        is an abstraction, behind which later we can have a SQL Accessor to
        get data from databases. The TransactionRecorderDataAccessor is
        the concrete implementation to access simulation transaction objects.
    '''
    def __init__(self, ta_recorder):
        self.ta_recorder = ta_recorder
    
    def get_transactions_in_period(self,start,end,account):
        #the data is actually stored in the TransactionRecorder,
        #a kind of database abstraction for in-memory objects.
        return self.ta_recorder.get_transactions(start, end, account)
        
        