import unittest

from lqn.core.accounts import Account

class TestAccount(unittest.TestCase):
"""
Test cases for the Account class
"""
    
    def setUp(self):
        print 'setting up'

    def tearDown(self):
        print 'tearing down'

    def testCreate(self):
        acc = Account(20)
        print "Getting balance"
        assert acc.getBalance() == 20

