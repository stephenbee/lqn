'''
Created on 13-lug-2009

@author: fabio
'''

#from typecheck import accepts
#from lqn.core.transactions import Transaction

class ValidationError(Exception):
    def __init__(self, dataobject, reason):
        self.dataobject = dataobject
        self.reason     = reason
        
    def __str__(self):
        msg = "Validation failed on object " + self.dataobject +  " - " + self.reason
        return repr(msg)


class DataValidator(object):
    '''
    Validates Transaction objects
    '''

    def validate(self,data):
        '''
        Constructor
        '''
        classname = data.__class__.__name__ + "Validator"
        clz = globals() [classname]
        validator = clz()
        if (issubclass(clz, self.__class__) ):
            validator.validate(data)
        else:
            raise ValidationError(data, "Validation on type " + type(data) + " is not yet implemented")
    
    
class TransactionValidator(DataValidator):
    '''
    Validates Transaction objects
    '''
    def validate(self,transaction):
        #print "Validating transaction"        
        validator = AccountValidator()
        validator.validate(transaction.get_credit_account())
        validator.validate(transaction.get_debit_account())
        validator = QuidValidator()
        validator.validate(transaction.get_amount())
        validator = DateValidator()
        validator.validate(transaction.get_date())
                
                        
class DateValidator(DataValidator):
    '''
    Validates date objects
    '''
    def validate(self,date):
        #print "Validating date"
        pass
        
        

class QuidValidator(DataValidator):
    '''
    Validates quid objects (amount)
    '''
    def validate(self,quids):
        #print "Validating quids"
        if (quids <= 0):
            raise ValidationError(type(self), "Quid amount must be greater than 0. Received: " + quids)



class AccountValidator(DataValidator):
    '''
    Validates account objects; does it exist? is it valid?
    '''
    def validate(self,account):
        #print "Validating account"
        pass