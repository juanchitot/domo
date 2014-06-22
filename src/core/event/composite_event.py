import string
from core.event.event import Event
from core.event.event_exception import EventException
from core.event.boolean_event import BooleanEvent
from core.event.timer_event import TimerEvent
from datetime import timedelta
from string import Template
import yaml

class CompositeEvent(Event):
    
    LOGICAL_SYMBOL = ['not','and','or']
    
    constructor_params = ['event_id','condition','events','reset_mode','reset_condition']
    
    def __init__(self,event_id,condition,events,reset_mode=False,reset_condition=""):
        Event.__init__(self,event_id)
        if not event_id:
            self.event_id = 'CE_%d' % self.event_id
        
        self.events = events
        self.condition = condition
        self.reset_condition = reset_condition
        self.reset_mode = reset_mode
#         self.params = {'event_id': "%s_%s" % (self.__class__.__name__,self.event_id)}
        
    def happend(self):
        happends = []
        happends_ids = []
        happends_dict = {}        
        for event in self.events:
            happends_ids.append(event.get_event_id())
            hap = int(event.happend())
            happends_dict[event.get_event_id()] = hap            
            happends.append(hap)
            
            Event.logger_instance.debug("%s %s %s %s" %  (self.event_id,
                                                          self.name,
                                                          self.condition,
                                                          happends_dict))
        Event.logger_instance.debug("happend [%s] %s %s" %  (self.event_id,     
                                                           string.join(happends_ids,','),
                                                           self.condition % tuple(happends)))
        
        status = eval(self.condition % tuple(happends))
        if self.reset_mode :
            reset = eval( self.reset_condition.substitute(happends_dict) )
#             Event.logger_instance.debug( self.reset_condition.substitute(happends_dict))
#             Event.logger_instance.debug("template %s valor %d " % (self.reset_condition.template,reset))            
            if reset :                
#                 Event.logger_instance.debug("reseteo composite event ")
                self.reset()
                
        return status
    
    def reset(self):
        for event in self.events :
            event.reset()
        
    def print_ports_id(self):
        for event in self.events:
            event.print_ports_id()

    def load_involved_ports(self,in_ports,out_ports):
#         print "load inv comp ev"
        for event in self.events :
#             print event.event_id
            event.load_involved_ports(in_ports,out_ports)
#             self.involved_ports.update(event.involved_ports)            
#             for port_id in event.involved_ports_id:
#                 if port_id not in self.involved_ports_id:
#                     self.involved_ports_id.append(port_id)
#                 self.involved_ports[port_id] = event.involved_ports[port_id]
#         print "-----"
    
    def edit(self,event):
        if not  isinstance(event,CompositeEvent):
            raise EventException("CompositeEvent.edit(%s), \
event no es un CompositeEvent" % self.event_id)
        if len(self.events) != len(event.events):
            raise EventException("CompositeEvent.edit(%s), \
distinta cantidad de events" % self.event_id)
        
        self.pause_delta = event.pause_delta
        self.paused_mode = event.paused_mode
        
        for pos in range(len(self.events)):
            self.events[pos].edit(event.events[pos])
    
    def get_params(self):
        return self.params

yaml.add_constructor(u'!CompositeEvent',CompositeEvent.yaml_constructor)
yaml.add_representer(CompositeEvent, CompositeEvent.yaml_representer)


if __name__ == '__main__' :    

    
    boolean = BooleanEvent('Bus_0_I_02_00',reverse=True)
    timer = TimerEvent(None,timedelta(seconds=5),None)
    timer.name = 'Timer de 15 segundos sin movimiento'
    
    reset_condition = Template('not $%s' % boolean.get_event_id())
    comp = CompositeEvent('%d and %d',[boolean,timer],True,reset_condition)
    comp.name = 'Hace 15 segundos que no hay movimiento'
    
    print yaml.dump(comp)
    dump = """!CompositeEvent
- - '%d and %d'
  - - !BooleanEvent
      - [Bus_0_I_02_00, true]
      - {}
    - !TimerEvent
      - []
      - {}
  - true
  - !!python/object:string.Template {template: not $BE_12397553851711870}
- {}
"""
    comp_l = yaml.load(dump)
    print yaml.dump(comp_l)


    
