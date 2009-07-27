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
            if (i.get_debit_account() == member):
                results.append(i)
        
        return results
        