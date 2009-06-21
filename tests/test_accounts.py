import unittest

from lqn.core.accounts import Account, InsufficientFunds

class TestAccount(unittest.TestCase):
    '''Test cases for the Account class'''

    def setUp(self):        
        self.acc = Account(20)
        
    def tearDown(self):
        pass

    def testCreate(self):
        self.assertEqual(self.acc.balance(), 20)

    def testInjectAndSubtract(self):
        self.acc.inject(70)
        assert self.acc.balance() == 90
        self.acc.extract(90)
        assert self.acc.balance() == 0

    def testExtractTooMuch(self):
        print 'Trying to extract too much'
        self.failUnlessRaises(InsufficientFunds, self.acc.extract, 70)
