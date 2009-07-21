from SimPy.Simulation import *
from lqn.core.accounts import Account
from lqn.core.transactions import Transaction, TransactionFailed

from activity import TransactionRecorder
from scenarios import *
from variables import *



class LqnMember(Process):
    '''
    A member in the LQN 
    '''
    def __init__(self, id, simInstance):
        Process.__init__(self)
        self.sim        = simInstance
        self.id         = id
        self.account    = Account(id)
        self.sim.activate(self,self.spend())
  
    def get_account(self):
        return self.account    
    
    # I register/initialize my membership  
    # while I am a quid user
    # I make a daily trade
    # I wait random days
    # if I have a reason to terminate my membership, leave the quid system
    def spend(self):
        while True:
            print self.sim.now(),self.id, ": I am spending."
            network.scenario.spend(self);
            wait_time = random.randrange(1.0,10.0)
            wait_time = float(wait_time)
            print self.id, ": Now I wait for",wait_time
            yield hold,self,wait_time
    
    
class LqnCouncilEmployee(LqnMember):
    '''
    There are members which are also employees
    of the council; they might get wages
    partly paid in quids.
    '''   
    def __init__(self, id, simInstance):
        LqnMember.__init__(self, id, simInstance)
        

class LqnBusiness(LqnMember):
    '''
    Every business owns an own account
    '''       
    def __init__(self, id, simInstance):
        LqnMember.__init__(self, id, simInstance)
        
        
        
class LqnTrust(Process):
    '''
    The trust managing the LQN; there is only one trust
    '''
    def __init__(self,name, simInstance):
        Process.__init__(self, simInstance)
        self.name = name
        self.account = Account(name)
        print self.name, "created."
        
    def create_initial_quids(self):
        #number or sponsors:
        sponsor_count = len(network.sponsors)
        #initial quids for members to start the sim
        total_member_quids = ( (num_of_members + num_of_employees) * \
                               initial_quids_per_account)
        #initial quids for businesses to start the sim
        total_business_quids = initial_quids_per_business * num_of_businesses
        #initial quids for sponsors to start the sim
        total_sponsors_quids = (initial_quids_per_account * \
                                sponsorship_factor * sponsor_count)
        #total initial quids to start the sim
        total_initial_quids = total_member_quids + total_sponsors_quids + \
                              total_business_quids
        #initial quid creation; crediting directly 
        #is only allowed for the trust        
        self.account.credit(total_initial_quids)
#       self.inject_quids(total_initial_quids)        
        #now credit every member account with a first transaction
        #with initial quids        
        self.__do_transactions(network.members, initial_quids_per_account)
        self.__do_transactions(network.employees, initial_quids_per_account)
        self.__do_transactions(network.sponsors, \
                             initial_quids_per_account * sponsorship_factor)
        self.__do_transactions(network.businesses, initial_quids_per_business)
        
        
        
    def __do_transactions(self,account_list,amount):
        for i in account_list:
            credit_account = i.get_account()
            timestamp = datetime.now()
            ta = Transaction(credit_account,self.account,amount,timestamp)
            ta.commit()
            network.ta_recorder.add_transaction(ta)

             
    def inject(self, account_list, amount):
        #first credit the trust account with the sufficient amount of quids
        count = len(account_list)
        total_amount = count * amount
        self.account.credit(total_amount)
#        self.inject_quids(total_amount)        
        self.__do_transactions(account_list, amount)        
        
        print "Injected",amount,"quids into",count,"accounts. Total:",\
                total_amount,"quids."                
#    def inject_quids(self, amount):
#        self.account.credit(amount)
#        yield put,self,total_quids_in_network,amount


class LqnNetwork(Process):
    '''
    Models the running of the whole LQN 
    '''
    def __init__(self, name, simInstance):
        Process.__init__(self, simInstance)
        self.sim            = simInstance
        self.name           = name
        self.members        = []
        self.employees      = []
        self.businesses     = []
        self.sponsors       = []
        self.all_members    = [self.members, self.employees, self.businesses, self.sponsors]
        self.total_quids    = 0
        #self.addedQuids     = 0
        self.ta_recorder    = TransactionRecorder()
        self.scenario       = SimpleScenario(self)
        #self.council_quids  = Monitor()
        #self.a_member_quids = Monitor()
        
    def create_network(self):
        self.trust = LqnTrust(self.name + " Trust" , self.sim)
        self.council = LqnMember("Kilkenny County Council", self.sim)
        self.sponsors.append(self.council)
        
        for i in range(num_of_members):
             self.members.append(LqnMember("Member-%d" %i, self.sim))
             
        for k in range(num_of_employees):
            self.employees.append(LqnCouncilEmployee("Employee-%d" %k, self.sim) )

        for n in range(num_of_businesses):
            self.businesses.append(LqnBusiness("Business-%d" %n, self.sim) )
            
        self.start();

    def start(self):
        random.seed(random_seed) # seeds the random number generator
        self.trust.create_initial_quids()
        self._calc_total_quids_in_network()
             
    def run(self):        
        while True:              
            day = self.sim.now()
            print "Current step is", day                    
            self.scenario.run(day)
            
            print "Total quids in network: ", total_quids_in_network.amount
            self._calc_total_quids_in_network()    
            yield hold,self,1.0
            
    def get_total_quids_in_network(self):
        return self.totalQuids

    #def check_simulation_goal(self):
    #    control = n*(s + t*(now() + 1) )
    #    print "Control (n*(s + t*(now() + 1) ): %d" %control
        
    def _calc_total_quids_in_network(self):
        self.total_quids = 0
        
        for list in self.all_members:
            for i in list:
                self.total_quids += i.get_account().get_balance()
        print "Total amount of quids in network: %d" %self.total_quids
     
    def _calc_total_quids_in_group(self, group):
        group_quids = 0               
        for i in group:
            group_quids += i.get_account().get_balance()
        return group_quids
     


#Run the simulation
sim = Simulation()
sim.initialize()
network = LqnNetwork("Kilkenny LQN", sim)
network.create_network()
sim.activate(network,network.run(),at=0.0)

total_quids_in_network = Level(name='total_quids_in_network', unitName='quids',
                               capacity='unbounded', initialBuffered=0,
                               monitored=True, monitorType=Monitor)

sim.simulate(until=90)


print "************************************************"
print "Simulation terminated"
print "Current time is ", sim.now()
#print "The quid level in the " + network.council.id + " account has been:"
#print network.council_quids.yseries()
#print "The quid level in the " + network.members[3].id + " account has been:"
#print network.a_member_quids.yseries()

    


