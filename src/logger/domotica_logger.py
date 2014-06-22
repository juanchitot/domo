import logging
import logging.handlers
import logging.config


logger_class = logging.getLoggerClass()

class DomoticaLogger(logger_class):
    
    def __init__(self,name):
        logger_class.__init__(self,name)
        
    
    def MiCustom(self):
        print  "Esta es mi clase customizada"

logging.setLoggerClass(DomoticaLogger) 
logging.config.fileConfig("logger/domotica_logging.conf")


    
    
