class Account():

    __quids = 0
    
    def __init__(self, initial_quids):
        self.__quids = initial_quids

    def getBalance(self):
        return self.__quids

    def uncoveredMethod(self):
        pass
