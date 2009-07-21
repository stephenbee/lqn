from lqn.core.accounts import Account, InsufficientFunds

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

    # These two attributes should be controllable by the simulation on the fly.
    # They should probably made threadsafe although the simulation gui will
    # initially have exclusive write access to them.
    _extraction_rate = 1
    _insertion_rate = 1
    
    def adjust(target_account):
        '''Requests a raw velocity report from an Account, then makes
        an appropriate transaction to extract or inject quids'''
        velocity_data = target_account.get_velocity_data()
        # Now apply the velocity algorithm.
        # Adjust the account accordingly using inject or extract methods.
        pass

