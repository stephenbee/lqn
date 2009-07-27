from lqn.core.accounts import Account, InsufficientFunds
from lqn.core.transactions import Transaction
from lqn.core import logger


class Policy(object):
    '''Policy encapsulates the money-supply policy for the LQN scheme.
    It makes transactions against accounts to add quids to performing
    accounts, and subract quids from non-performing accounts.
    Policy parameters can be controlled from the simulation GUI in real
    time.

    The simulation should possibly be able to select between algorithms.

    Policy should have an account for doing transactions so that we can
    do sanity checking on the system.
    '''
    observation_start   = 0
    observation_end     = 0    
    # These two attributes should be controllable by the simulation on the fly.
    # They should probably made threadsafe although the simulation gui will
    # initially have exclusive write access to them.
    _extraction_rate = 1
    _insertion_rate = 1
    
    def apply(self, target_account):
        '''Requests a raw velocity report from an Account, then makes
        an appropriate transaction to extract or inject quids'''
        velocity_data = target_account.get_velocity_data()
        # Now apply the velocity algorithm.
        # Adjust the account accordingly using inject or extract methods.
        pass


class SimplePolicy(Policy):
    '''
    In the SimplePolicy, the total amount of transactions over the
    observation period is checked. 
    If (total_transaction_amounts_in_period   <    current_balance)
        then detract_quids from account
    If (total_transaction_amounts_in_period   =    current_balance)
        then nothing happens
    If (total_transaction_amounts_in_period   <    current_balance)
        then inject_quids into account
        
    The adjustment rate is 10% of current_balance
    '''    
    def apply(self, trust_account, target_account, data_accessor, date):
        current_balance = target_account.get_balance()
        transactions    = data_accessor.\
                            get_transactions_in_period(self.observation_start, 
                                                       self.observation_end,
                                                       target_account)
        
        amount = current_balance / 10
        quids_level = amount
        
        if (transactions is None):
            total_transaction_amounts_in_period = 0            
        else:
            for i in transactions:
                total_transaction_amounts_in_period += i.get_amount
            
        if ( (total_transaction_amounts_in_period < current_balance) and
                (amount != 0)) :
            if (current_balance < amount):
                amount = current_balance
            ta = Transaction(trust_account, target_account, amount, date)
            ta.commit()
            logger.info("Policy applied. Removed %d quids from user account %s.",
                       amount, target_account.get_account_holder())
            quids_level = -1*amount
            
        elif ( (total_transaction_amounts_in_period == current_balance) or
                (amount == 0) ):
            logger.info("Policy applied: No changes necessary.")
            quids_level = 0
        else: # (total_transaction_amounts_in_period > current_balance):
            trust_account.credit(amount)
            ta = Transaction(target_account, trust_account, amount, date)
            ta.commit()
            logger.info("Policy applied. Injected %d quids to user account %s.",
                        amount, target_account.get_account_holder())
        
        return quids_level


                                                                   
class TransactionDataAccessor(object):
    
    def get_transactions_in_period(self,start_date, end_date, account):
        pass
    
