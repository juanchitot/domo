

import time
import yaml

from core.event.event import Event
from core.event.event_exception import EventException
from datetime import datetime, timedelta 

class BooleanEvent(Event):
    
    constructor_params = ['event_id','port_id','reverse'] 
   
    def __init__(self,event_id,port_id,reverse=False):
        Event.__init__(self,event_id)
        if not event_id :
            self.event_id = 'BE_%d' % self.event_id

        self.involved_ports_id.append(port_id)
        self.port_id = port_id
        self.reverse = reverse
        
    def reset(self):
        pass
    
    def happend(self):
        if not self.initialized :
            raise EventException("El evento %s no esta inicializado" % self.event_id)
        
        port_id = self.involved_ports_id[0]
        port = self.involved_ports[port_id]
        Event.logger_instance.debug("port_id %s objectid %s " %  ( port_id,id(port) ))
        
        ret = False        
        if not self.reverse and port.get_value() :
            ret =  True
        elif self.reverse and not port.get_value() :            
            ret = True
        
        Event.logger_instance.debug("happend [%s] %s %s %s" %  (self.event_id,    
                                                                ret,
                                                                port.get_value(),
                                                                self.reverse))
        return ret
    
    def get_params(self):
        port_id = self.involved_ports_id[0]
        port = self.involved_ports[port_id]
        self.params['ports'] = { port : port.get_value() }
        return self.params
    
yaml.add_constructor(u'!BooleanEvent',BooleanEvent.yaml_constructor)
yaml.add_representer(BooleanEvent, BooleanEvent.yaml_representer)
