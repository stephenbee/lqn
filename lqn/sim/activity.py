'''
Created on 13-lug-2009

@author: fabio
'''

class TransactionRecorder(object):
    '''
    Acts as database replacement for the simulation
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.transactions = list()

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        
    def get_transactions(self, start_date, end_date, member):
        results = list()
        for i in self.transactions:
            #print "debit_account: %s, member: %s" %(i.get_debit_account(),member)
            if (i.get_debit_account() == member):
                #print "Found"
                results.append(i)
        
        return results

class AccountHistory(object):
    '''
    Interface to access account history -should maybe go to Account class?
    '''
    def process_daily_balance(self, balance, accounts):
        for account in accounts:
            balance = account.get_balance()
            
    
    def get_average_balance(self,account):
        pass
    
            