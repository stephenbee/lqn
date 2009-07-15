from SimPy.Simulation import *
from lqn.core.accounts import Account
from lqn.core.transactions import Transaction, TransactionFailed
from datetime import datetime
from activity import TransactionRecorder

import random

class LqnMember(Process):
    '''
    A member in the LQN 
    '''
    def __init__(self, id):
        Process.__init__(self)
        self.id = id
        self.account = Account(id)
        #self.account.credit(s)  #Initial quids injection should be a transaction
                                 #and done through the trust   
        
    def get_account(self):
        return self.account
    
    
    
class LqnTrust(Process):
    '''
    The trust managing the LQN; there is only one trust
    '''
    def __init__(self,name):
        Process.__init__(self)
        self.name = name
        self.account = Account(name)
        print self.name, "created."
        
    def create_initial_quids(self, network):
        #number or sponsors:
        sponsor_count = len(network.sponsors)
        #initial quids for members to start the sim
        total_member_quids = (num_of_accounts * initial_quids_per_account)
        #initial quids for sponsors to start the sim
        total_sponsors_quids = (initial_quids_per_account * \
                                sponsorship_factor * sponsor_count)
        #total initial quids to start the sim
        total_initial_quids = total_member_quids + total_sponsors_quids
        #initial quid creation; crediting directly 
        #is only allowed for the trust        
        self.account.credit(total_initial_quids)
        #now credit every member account with a first transaction
        #with s initial quids
        
        self.do_transactions(network.members, initial_quids_per_account)
        self.do_transactions(network.sponsors, \
                             initial_quids_per_account * sponsorship_factor)
        
        
    def do_transactions(self,account_list,amount):
        for i in account_list:
            credit_account = i.get_account()
            timestamp = datetime.now()
            ta = Transaction(credit_account,self.account,amount,timestamp)
            ta.commit()
            network.ta_recorder.add_transaction(ta)
             
    def inject_quids(self):
        pass
    
    def withdraw_quids(self):
        pass



class LqnNetwork(Process):
    '''
    Models the running of the whole LQN 
    '''
    def __init__(self, name):
        Process.__init__(self)
        self.name           = name
        self.members        = []
        self.totalQuids     = 0
        self.addedQuids     = 0
        self.ta_recorder    = TransactionRecorder()
        self.sponsors       = []
        
    def create_network(self):
        self.trust = LqnTrust(self.name + " Trust" )
        self.council = LqnMember("Kilkenny County Council")
        self.sponsors.append(self.council)
        
        for i in range(num_of_accounts):
             self.members.append(LqnMember("Member-%d" %i))
        
        
    def start(self):
        random.seed() # seeds the random number generator
        self.trust.create_initial_quids(self)
        self._calc_total_quids_in_network()
        
    def day(self):
        for i in self.members:
            #for now, just pick another member as credit_account, at random 
            index = random.randint(0,len(self.members)-1) # ta takes place with existing businesss
            creditor = self.members[index]
            credit_account = creditor.get_account()
            #create a ta amount at random
            ta_amount = random.randrange(lower_range_transaction,  
                                         upper_range_transaction)
            #timestamp
            tstamp = datetime.now()
            ta = Transaction(credit_account,i.get_account(),ta_amount,tstamp)
            try:
                ta.commit()
                self.ta_recorder.add_transaction(ta)
            except TransactionFailed:
                #do nothing for now
                pass
            #i.earnQuids(t)
            #self.addedQuids = self.addedQuids + t
            council_quids.observe(self.council.account.get_balance())
            a_member_quids.observe(self.members[3].account.get_balance())
            
    def week(self):
        pass
    
    def month(self):
        pass
             
    def run(self):
        
        while (1):
            day = now()
            print "Current step is", day
            
            self.day()
                
            if day % 7 == 0 : #this is also end of week
                self.week()
            
            if day % 30 == 0: #this is also end of month
                self.month()
                
            self._calc_total_quids_in_network()    
            yield hold,self,1.0
            
    def get_total_quids_in_network(self):
        return self.totalQuids

    def check_simulation_goal(self):
        control = n*(s + t*(now() + 1) )
        print "Control (n*(s + t*(now() + 1) ): %d" %control
        
    def _calc_total_quids_in_network(self):
        self.totalQuids = 0
        for i in self.members:
            self.totalQuids = self.totalQuids + i.get_account().get_balance()
        for i in self.sponsors:
            self.totalQuids = self.totalQuids + i.get_account().get_balance()
        #if self.totalQuids >= I:
        #    stopSimulation()
        #    self.checkSimulationGoal()
        print "Total amount of quids in network: %d" %self.totalQuids
 
 
#global variables for the simulation   

#number of accounts
num_of_accounts             = 10
 #initial quids amount per member account            
initial_quids_per_account   = 100
#increase step, in quids
increase_step               = 20
#final total quids amount, not used for now            
final_total_quids           = 100000
#sponsorship factor         
sponsorship_factor          = 10000
#every transaction gets randomly a value between
#lower_range_transaction and upper_range_transaction                
lower_range_transaction     = 10            
upper_range_transaction     = 100           


#Run the simulation
initialize()
network = LqnNetwork("Kilkenny LQN")
network.create_network()
network.start()
council_quids  = Monitor()
a_member_quids = Monitor()
activate(network,network.run(),at=0.0)
simulate(until=100)
print "************************************************"
print "Simulation terminated"
print "Current time is ", now()
print "The quid level in the " + network.council.id + " account has been:"
print council_quids.yseries()
print "The quid level in the " + network.members[3].id + " account has been:"
print a_member_quids.yseries()

    


