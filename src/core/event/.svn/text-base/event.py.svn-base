import logging
import time
from datetime import datetime, timedelta 
from configurator.domotica_serialize import DomoticaSerialize
from core.domotica_exception import DomoticaException

class Event(DomoticaSerialize):
    
    logger_instance = logging.getLogger('domotica.real_time_core.event')

    constructor_params = ['event_id']
    serializable_data = {'name':'name','comment':'comment'}

    def __init__(self,event_id=None):
        if event_id:
            self.event_id = event_id            
        else:
            self.event_id = int(time.time()*10000000)
        
        self.name = ''
        self.comment = ''
        
        self.involved_ports_id = []
        self.involved_ports = {}
        self.enabled = True
        # - cada vez que se chequea con happend si sucedio el evento
        #   y este esta en paused_mode = True se pausa pause_delta el evento
        self.pause_delta = timedelta()
        self.paused_mode = False
        self.paused_since = False

        self.params = {'event_id': "%s_%s" % (self.__class__.__name__,self.event_id)}
        self.initialized = False
        self.times_fired = 0
        self.times_to_fire = 0
        
    def get_event_id(self):
        return self.event_id
    
    def happend(self):
        raise NotImplementedError('event.py: metodo abstracto happend no implementado')
    
    def fired_one_more_time(self):
        self.times_fired += 1
    
    def get_params(self):
        raise NotImplementedError('event.py: metodo abstracto get_params no implementado')
    
    def enable(self):
        self.enabled = True
        
    def disable(self):
        self.enabled = False
	        
    def pause(self,delta=None):
        self.paused_since = datetime.now()
        if delta:
            self.pause_delta = delta
        
    def is_paused(self):        
        if not self.paused_since:
            return False
        now = datetime.now()
        if (self.paused_since + self.pause_delta) > now :
            return True
        
        return False
    
    def reset(self):
        raise NotImplementedError('event.py: metodo abstracto reset no implementado')
        
    def print_ports_id(self):
        print "Event ports %s " % self.name
        st=""
        for p_k, p in  self.involved_ports.items():
            st += " (%s,%d)" % (p_k,id(p))
        print st
        
    def load_involved_ports(self,in_ports,out_ports):
        missing_ports = 0
        missing_ports_keys = ''
        for port_id in self.involved_ports_id:
            if port_id in in_ports:
                self.involved_ports[port_id] = in_ports[port_id]
            elif port_id in out_ports:
                self.involved_ports[port_id] = out_ports[port_id]
            else:
                missing_ports += 1
                missing_ports_keys += ' %s' % port_id 
        
        if missing_ports :
            print "faltan puertos"
            raise EventException("Error: al evento %s le faltan los puertos %s" % (self.event_id,missing_ports_keys))
 
        
        # for port in ports:
        #             if port.get_id() in self.involved_ports_id :
        #                 self.involved_ports[port.get_id()] = port        
        # if len(self.involved_ports_id) <> len(self.involved_ports):
        #                     pass
        #             #raise exeption
        self.initialized = True
    
    def edit(self, event):
        pass
#         print "hago un edit del evento %s" % self.event_id
        

class EventException(DomoticaException):
    pass
