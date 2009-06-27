import unittest

from lqn.core.accounts import Account, InsufficientFunds

class TestAccount(unittest.TestCase):
    '''Test cases for the Account class'''

    def setUp(self):        
        self.acc = Account("me")
        
    def tearDown(self):
        pass
    
    def testCreate(self):
        assert self.acc._accountholder is not None

    def testDebitAndCredit(self):
        self.acc.credit(70)
        assert self.acc.getBalance() == 70
        self.acc.debit(70)
        assert self.acc.getBalance() == 0
        self.acc.credit(40)
        self.acc.credit(60)
        assert self.acc.getBalance() == 100

    def testExtractTooMuch(self):
        print 'Trying to extract too much'
        self.failUnlessRaises(InsufficientFunds, self.acc.debit, 70)

        
class TestAccountNumberGenerator(unittest.TestCase):
    
    def setUp(self):
        self.accounts = [Account("me"), Account("you"), Account("her")]
        
    def testNumberGeneration(self):
        nums = []
        for acc in self.accounts:
            num = acc.getAccountNumber()
            assert num is not None #check that account number is not None
            assert num not in nums #check if the accountnumber is unique (would probably need better or at least more test...)
            nums.append(num)
            #self.assertEqual(num, count, "Unexpected account number, expecting %d, got %d" % (count, num))
    

if __name__ == "__main__":
    unittest.main()   
         
#test = TestAccountNumberGenerator()
#test.setUp()
#test.runTest()
