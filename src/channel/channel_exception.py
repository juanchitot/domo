from core.domotica_exception import DomoticaException

class ChannelException(DomoticaException):
    pass


if __name__ == '__main__' :
    
    print "Hago un raise"
    try:
        raise ChannelException("parm1","parm2")
    except Exception, e:
        print "Levanto la Excepcion"
        print e
    print "sali"
