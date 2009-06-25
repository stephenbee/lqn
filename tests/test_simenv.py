import unittest

from lqn.sim.simenv import SimEnv

class TestAccount(unittest.TestCase):
    '''Test cases for the SimEnv class'''

    def setUp(self):        
        self.simenv = SimEnv(100, 100, 0.1)
 
    def tearDown(self):
        pass

    def testTradingPropensity(self):
        pass

    def testPriceDistribution(self):
        pass
