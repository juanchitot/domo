import logging
import time
from configurator.domotica_serialize import DomoticaSerialize
from core.action.action_exception import ActionException
class Action(DomoticaSerialize):
    
    logger_instance = logging.getLogger('domotica.real_time_core.action')

    constructor_params = ['action_id']
    serializable_data = {'name':'name','comment':'comment'}

    def __init__(self,action_id=None):
        if action_id:
            self.action_id = action_id
        else:
            self.action_id = int(time.time()*10000000)
        
        self.name = ''
        self.comment = ''
        
        self.involved_ports = {}
        self.involved_ports_id = []
        
        self.params = {}
        
        self.executed = False
        self.done = False
        self.ports_loaded = False
    
    def get_action_id(self):
        return self.action_id
    
    def execute(self,params={}): 
        
        Action.logger_instance.debug("ejecuto la accion con params %s " % self.params)
        self.done = True
        self.executed = True
    
    def done(self):
        return self.done
        
    def load_involved_ports(self,ports):
        missing_ports = 0
#         print "load ports action %s (%d)" % (self.__class__.__name__,len(self.involved_ports_id))
        for port_id in self.involved_ports_id:
            if port_id in ports:
                self.involved_ports[port_id] = ports[port_id]
            else:
                missing_ports += 1
        
        if missing_ports :
            raise ActionException('La accion %s posee %d puertos faltantes' % (self.action_id,missing_ports))        
        self.ports_loaded = True
    
    def print_ports_id(self):
#         print "Action ports %s %d" % (self.name,len(self.involved_ports))
        st=""
        for p_k, p in  self.involved_ports.items():
            st += " (%s,%d)" % (p_k,id(p))
        print st
