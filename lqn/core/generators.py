'''
Created on 13-lug-2009

@author: fabio
'''
#class AccountNumberGeneratorFactory(object):
    
class AccountNumberGenerator(object):    

    def __init(self):        
        self.set(generator)

    #def set(self, generator):
    #    self.__generator = generator

    def generate(self):
        raise Exception("Error: Only AccountNumberGenerator subclasses implement generate()")
    
    
    
class IncrementalGenerator(AccountNumberGenerator):
    
    __counter=0
    
    def generate(self):
        self.__counter += 1
        return self.__counter
    
#default_generator = IncrementalGenerator    
account_number_generator = IncrementalGenerator()