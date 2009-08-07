from lqn.core.generators import account_number_generator
from lqn.core import logger

from collections import deque 

class InsufficientFunds(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Account(object):
    
    '''Implements an LQN account.  Note that murrage and demurrage
    are taken care of elsewhere in the Policy class'''
    
    def __init__(self, holder):
        self.__accountnumber    = self.__generate_account_number()
        self.__accountholder    = holder
        self.__balance          = 0
        self.account_history   = AccountHistory(90)
        logger.debug("Created account number %d for %s ", self.__accountnumber, holder)
        
    def __generate_account_number(self):
        return account_number_generator.generate()
        
    def get_account_number(self):
        return self.__accountnumber
    
    def get_account_holder(self):
        return self.__accountholder
    
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
     

  
class AccountHistory(object):
    '''
        This class is used to store daily balances of accounts.
        It is very appropriate also to think to attach this functionality
        directly onto the account. But as the current algorithm for
        velocity calculation is still evolving, we want to keep the
        Account class as pure as possible for now.
    '''
    
    def __init__(self, max_period):
        self.daily_history  = deque(maxlen=max_period)
        self.period         = max_period
        
    def record_daily_balance(self, amount):
        '''
        Store the daily balance of a particular account. Should be
        the end-of-day balance, but for matters of simulation, it is
        ok to just have one storage call per day.
        '''        
        self.daily_history.append(amount)
        if (len(self.daily_history) > self.period):
            self.daily_history.popleft()
    
    def get_average_balance(self):
        '''
        Return the mean average balance for this account
        '''
        balance_sum = sum(self.daily_history)
        divisor = self.period
        if (len(self.daily_history) < self.period):
            divisor = len(self.daily_history)
        return balance_sum / float (divisor)


class AccountType(object):
    '''
    Not used yet, maybe later or maybe obsolete.
    '''
    Business, Member, Trust, Sponsor = range(4)