'''
Created on 13-lug-2009

@author: fabio
'''

from lqn.core.validators import DataValidator
from lqn.core.accounts import InsufficientFunds

class TransactionFailed(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value) 

class Transaction(object):
    '''
    Encapuslates a transaction. A transaction is 
    any movement of quid from an Account instance to another
    '''


    def __init__(self,credit_account, debit_account, amount, date):
        '''
        Constructor
        '''
        self.__credit_account = credit_account;
        self.__debit_account  = debit_account;
        self.__amount         = amount;
        self.__date           = date;
        
        validator           = DataValidator();
        validator.validate(self);
        
    def get_credit_account(self):
        return self.__credit_account;
    
    def get_debit_account(self):
        return self.__debit_account;
    
    def get_amount(self):
        return self.__amount;
    
    def get_date(self):
        return self.__date;
    
    def commit(self):
        '''
        Perform the transaction.
        If debit fails (e.g. not enough balance),
        transaction fails
        '''
        try:
            self.__debit_account.debit(self.__amount)
            self.__credit_account.credit(self.__amount)
        except InsufficientFunds:
            msg = "Transaction failed. Not sufficient funds on debit account "
            print msg
            raise TransactionFailed(msg)
        
        
        
        
    