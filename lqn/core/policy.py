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
    If (total_transaction_amounts_in_period   <    average_balance)
        then detract_quids from account
    If (total_transaction_amounts_in_period   =    average_balance)
        then nothing happens
    If (total_transaction_amounts_in_period   <    average_balance)
        then inject_quids into account
        
    The adjustment rate is 5% of current_balance.
    This rate should be adjustable, probably a variable. However,
    currently the variables module is in the simulation. For now,
    we want to keep simulation and core really separate.
    '''
    adjustment_rate = 0.05
       
    def apply(self, trust_account, target_account, data_accessor, date):
        #get the current balance
        current_balance = target_account.get_balance()
        if (current_balance == 0):
            logger.info("Policy cannot be applied: current balance is 0.")
            return 0;
        
        # get the average balance
        average_balance = target_account.account_history.get_average_balance()
        logger.info("Average balance for account %s: %d", 
                    target_account.get_account_holder(),
                    average_balance)
        #get all transactions for this account in the observation period
        transactions    = data_accessor.\
                            get_transactions_in_period(self.observation_start, 
                                                       self.observation_end,
                                                       target_account)
        #how much will be adjusted
        amount = average_balance * self.adjustment_rate
        #quids_level is just a variable to store the return value from this
        #method, and could be negative or positive.
        quids_level = amount
        #the sum of all transaction amounts in the observation period 
        total_transaction_amounts_in_period = 0
        
        #no transactions have been found 
        if (transactions is not None):            
            logger.debug("Transactions are available.")
            for i in transactions:
                total_transaction_amounts_in_period += i.get_amount()
            logger.debug("Total transactions in period for %s: %d",
                         target_account.get_account_holder(),
                         total_transaction_amounts_in_period)
        else:
            logger.warn("Transaction are None!")
                
        
        #if this rule applies, quids will be detracted
        if ((total_transaction_amounts_in_period < average_balance) and
            amount >0) :
                #we cannot detract more than there is on the current balance
                if ( current_balance < amount):
                    amount = current_balance
                #create the transaction and commit
                ta = Transaction(trust_account, target_account, amount, date)
                ta.commit()
                logger.info("Policy applied. Removed %d quids from user account %s.",
                      amount, target_account.get_account_holder())
                quids_level = -1*amount #so actually we have a negative amount
        #if this rule applies, there's nothing to do (this is arbitrary and
        #may be total nonsense)
        elif ( (total_transaction_amounts_in_period == average_balance) or
                (amount == 0) ):
            logger.info("Policy applied: No changes necessary.")
            quids_level = 0
        #if this rule applies, quies will be injected
        else: # (total_transaction_amounts_in_period > average_balance):
            #first the trust needs to CREATE the quids in wants to inject
            trust_account.credit(amount)
            #then create the transaction and commit
            ta = Transaction(target_account, trust_account, amount, date)
            ta.commit()
            logger.info("Policy applied. Injected %d quids to user account %s.",
                        amount, target_account.get_account_holder())
        
        return quids_level


                                                                   
class TransactionDataAccessor(object):
    '''
    To access transactions, this is an abstraction class. Implementations
    then should implement this interface. The production system will have
    a database where transactions will be stored, while the simulation
    for example stores objects in memory.
    '''
    def get_transactions_in_period(self,start_date, end_date, account):
        pass
    