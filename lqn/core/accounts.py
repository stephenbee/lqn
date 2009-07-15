from lqn.core.generators import account_number_generator

class InsufficientFunds(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Account(object):
    
    '''Implements an LQN account.  Note that murrage and demurrage
    are taken care of elsewhere in the Policy class'''
    
    def __init__(self, holder):
        self.__accountnumber = self.__generate_account_number()
        self.__accountholder = holder
        self.__balance = 0
        print "Created account number %d for %s " % (self.__accountnumber, holder)
        
    def __generate_account_number(self):
        return account_number_generator.generate()
        
    def get_account_number(self):
        return self.__accountnumber
    
    def get_balance(self):
        '''balance getter'''
        return self.__balance

    def credit(self, amount):
        self.__balance += amount

    def debit(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
        else:
            raise InsufficientFunds, self.__balance    
    

