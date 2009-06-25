class SimEnv(object):
    """
    This class encapsulates the simulated world used in the simulation
    of LQN.  It controls:
    - The price distribution of services
    - The ticks between policy intervention
    - Growth rate of users
    - propensity to trade

    Although there are initial values at least some parameters should be
    adjustable 'on the fly' during the simulation.
    """

    _max_price       # Maximum price in the distribution
    _ticks_between_policy # Determines how often accounts are adjusted
    _overall_trading_propensity # Determines probability that account trades
    
    def __init__(self, max_price, ticks_between_policy, trading_propensity):
        _max_price = max_price
        _ticks_between_policy = ticks_between_policy
        _overall_trading_propensity = trading_propensity

    def getPrice(self):
        """Returns a random price for a trade based on a probability
        distribution and the maximum price.  Initially we'll go for a gaussian
        distribution although a gamma distribution might be more realistic"""
        pass

    
