import logging
import sys
import os
import string
import traceback

class DomoticaException(Exception):
    
    def __init__(self,msg, tb=None, *args):
        
        if isinstance(msg,Exception):
            self.message = repr(msg)
        else:
            self.message = msg
        
        self.args = args
        self.tb_text = ''
        if tb:
            self.set_tb(tb)
        else:
            (et,ev,tb) = sys.exc_info()
            if tb:
                self.set_tb(tb)
        
    def log(self,local_logger=None):
        log_msg = "%s \n %s" % (self.message,self.tb_text)
        if local_logger :
            local_logger.log(logging.ERROR, log_msg)
        else:
            base_logger = logging.getLogger('domotica.exceptions.%s' % self.__class__.__name__)
            base_logger.log(logging.ERROR, log_msg)
            
    def __repr__(self):
        return "%s, %s\n %s, %s " % (self.tb_text,
                                     str(self.args),
                                     self.__class__.__name__,
                                     self.message)

    
    def set_tb(self,tb_obj):
        tmp = os.tmpfile()
        traceback.print_tb(tb_obj,None,tmp)
        tmp.seek(0)
        self.tb_text = string.join(tmp.readlines(),"")

class StaticClassException(DomoticaException):
    pass
