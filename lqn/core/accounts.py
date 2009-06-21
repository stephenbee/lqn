class InsufficientFunds(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Account(object):
    
    '''Implements an LQN account.  Note that murrage and demurrage
    are taken care of elsewhere in the Policy class'''
    
    _balance = 0 
    
    def __init__(self, initial_balance):
        self._balance = initial_balance
    
    def balance(self):
        '''balance getter'''
        return self._balance

    def inject(self, amount):
        self._balance += amount

    def extract(self, amount):
        if amount <= self._balance:
            self._balance -= amount
        else:
            raise InsufficientFunds, self._balance

    def get_velocity_data(self):
        '''Return raw velocity over a certain time period.
        This may take the form of a list of transaction amounts.

        This method should probably have a start and end time'''
        pass
    
    
