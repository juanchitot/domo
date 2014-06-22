
import yaml

from action import Action
from core.action.action_exception import ActionException

class SetterAction(Action):
    
    MODE_SET = 1 
    MODE_CLEAR = 2
    MODE_TOGGLE = 3
    
    constructor_params = ['action_id','involved_ports_id','mode']
    seriarizable_data = {'inverted_ports':'inverted_ports'}
    
    def __init__(self,action_id,ports_id,mode=1):
        Action.__init__(self,action_id)
        
#         print "creo setteraction %s" % str(ports_id)
        self.inverted_ports = {}
        if type(ports_id) == dict :
            self.involved_ports_id = ports_id.keys()                
            self.inverted_ports = [ k for k,v in ports_id.items()  if v ]
        else:
            self.involved_ports_id = ports_id
        self.mode = mode
        
    def execute(self):
        Action.logger_instance.debug("entro al execute de la accion %s " % self.action_id )
        if not self.ports_loaded :
            raise ActionException("Error: faltan puertos, id(%s),name(%s)" %  (self.action_id,self.name))
        
        self.logger_instance.debug("entro al execute de la accion %s " % self.action_id )
        for port_id in self.involved_ports_id :
            port = self.involved_ports[port_id]
            
            if self.mode == SetterAction.MODE_TOGGLE :
                port.value = int(not port.value)
            else:
                if self.mode == SetterAction.MODE_CLEAR :
                    value = 0 
                else :
                    value = 1
                if port_id in self.inverted_ports :
                    value = int(not value)
                port.value = value
                
            
yaml.add_constructor(u'!SetterAction',SetterAction.yaml_constructor)
yaml.add_representer(SetterAction, SetterAction.yaml_representer)
