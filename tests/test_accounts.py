import unittest

from lqn.core.accounts import Account

class TestAccount(unittest.TestCase):

    def setUp(self):
        print 'setting up'

    def tearDown(self):
        print 'tearing down'

    def testCreate(self):
        acc = Account(20)
        print "Getting balance"
        assert acc.getBalance() == 20

