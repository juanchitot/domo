from core.domotica_exception import DomoticaException

class CardException(DomoticaException):    
    READ_OPERATION = 1
    WRITE_OPERATION = 2
    TEST_OPERATION = 3
    RESET_OPERATION = 4
    

class CardResponseException(CardException):
    
    def __repr__(self):
        print "este es el repr de cardresponseexception"

class CardTimeoutException(CardException):
    pass
