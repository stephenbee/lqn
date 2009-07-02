from SimPy.Simulation import *
from lqn.core.accounts import Account

class LqnMember(Process):
    def __init__(self, id):
        Process.__init__(self)
        self.id = id
        self.account = Account(id)
        self.account.credit(s)
    
    def earnQuids(self, quids):
        print now(), self.id, " got quids in the account"
        self.account.credit(quids)
        
    def getAccount(self):
        return self.account

class LqnNetwork(Process):
    
    def __init__(self, name):
        Process.__init__(self)
        self.name = name
        self.members = []
        self.totalQuids = 0
        
    def createNetwork(self):
        for i in range(n):
             self.members.append(LqnMember("Member-%d" %i))
        self._calcTotalQuidsInNetwork()
             
    def quidInjection(self):
        while (1):
            for i in self.members:
                i.earnQuids(t)
            self._calcTotalQuidsInNetwork()    
            yield hold,self,1.0   

    def _calcTotalQuidsInNetwork(self):
        self.totalQuids = 0
        for i in self.members:
            self.totalQuids = self.totalQuids + i.getAccount().getBalance()
        print "Total amount of quids in network: %d" %self.totalQuids
    
           
n = 10      #number of accounts
s = 1000    #initial quids amount per account
t = 20      #increase step, in quids
I = 100000  #final total quids amount     


initialize()
network = LqnNetwork("Dublin Regional Authority")
network.createNetwork()
activate(network,network.quidInjection(),at=0.0)
simulate(until=100)
print "Current time is ", now()
    


