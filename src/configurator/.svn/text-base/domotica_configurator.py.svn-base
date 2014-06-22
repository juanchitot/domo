import yaml
import sys
import os
import os.path
from configurator.configurator_exception import ConfiguratorException
from core.domotica_exception import DomoticaException

class DomoticaConfigurator:
    
    def __init__(self, config_file):        
        self.main_config_file = config_file
    
    def initialize(self,domotica):
        pass

    def load_configuration(self):
        try :
            self.open_conf_file('r')            
#             self.conf_file = open(DomoticaConfigurator.MAIN_CONFIG_FILE + '.bak','r')
            return yaml.load(self.conf_file) 
        except Exception:
            raise ConfiguratorException('No se pudo leer la configuracion')            
    
    def save_configuration(self,save_data):
        name = self.main_config_file 

        if self.conf_file :
            self.conf_file.close()
        
        if os.path.exists("%s.5" % name) :
            os.unlink("%s.5" % name)
        
        for i in reversed(range(5)):
            src = "%s.%d" % (name,i)
            dst = "%s.%d" % (name,i+1)
            
            if os.path.exists(src) :
                os.rename(src,dst)
        
        src = "%s" % name
        dst = "%s.%d" % (name,0)
        
        if os.path.exists(src) :
            os.rename(src,dst)
        
        self.open_conf_file('w')
        
        try :
             yaml.dump(save_data,self.conf_file) 
        except Exception, e:
            raise ConfiguratorException('No se pudo guardar la configuracion %s' % e.message)
        
    def open_conf_file(self,mode):
        try :
            self.conf_file = open(self.main_config_file,mode)
        except IOError:
            self.conf_file = None
            raise ConfiguratorException('No se pudo abrir el archivo de configuracion')
