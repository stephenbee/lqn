class InsufficientFunds(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Account(object):
    
    '''Implements an LQN account.  Note that murrage and demurrage
    are taken care of elsewhere in the Policy class'''
    
    def __init__(self, holder):
        self._accountnumber = self._generateAccountNumber()
        self._accountholder = holder
        self._balance = 0
        print "Created account number %d for %s " % (self._accountnumber, holder)
        
    def _generateAccountNumber(self):
        return AccountNumberGenerator.generate()
        
    def getAccountNumber(self):
        return self._accountnumber
    
    def getBalance(self):
        '''balance getter'''
        return self._balance

    def credit(self, amount):
        self._balance += amount

    def debit(self, amount):
        if amount <= self._balance:
            self._balance -= amount
        else:
            raise InsufficientFunds, self._balance

    def get_velocity_data(self):
        '''Return raw velocity over a certain time period.
        This may take the form of a list of transaction amounts.

        This method should probably have a start and end time'''
        pass
    
    
class AccountNumberGenerator(object):
    
    _generatorCls = "IncrementalGenerator"
    
    def generate():
        cls = globals()[AccountNumberGenerator._generatorCls]
        return cls.generate()
    generate = staticmethod(generate)
    
    
    
class IncrementalGenerator(object):
    
    _counter=0
    
    def generate():
        IncrementalGenerator._counter = IncrementalGenerator._counter + 1
        return IncrementalGenerator._counter
    generate = staticmethod(generate)
    
