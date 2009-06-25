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
    
    def __init__(self, max_price, ticks_between_policy, trading_propensity):
        # Maximum price in the distribution
        self._max_price = max_price
        # Determines how often accounts are adjusted
        self._ticks_between_policy = ticks_between_policy
        # Determines probability that account trades during a tick
        self._overall_trading_propensity = trading_propensity

    def get_price(self):
        """Returns a random price for a trade based on a probability
        distribution and the maximum price.  Initially we'll go for a gaussian
        distribution although a gamma distribution might be more realistic
        See http://docs.python.org/library/random.html
        """
        pass

    def graph_price_distribution(self):
        """Helper class to display distribution"""
        pass
