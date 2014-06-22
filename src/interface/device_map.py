import yaml
import time
import string 

from datetime import timedelta

from core.event.boolean_event import BooleanEvent
from core.event.composite_event import CompositeEvent
from core.action.setter_action import SetterAction
from core.event.timer_event import TimerEvent
from string import Template 

from configurator.domotica_serialize import DomoticaSerialize



class DeviceMap(DomoticaSerialize):
    
    serializable_data = {'id' : 'id',
                         'name':'name',
                         'comment':'comment',
                         'sensors_ports':'sensors_ports',
                         'light_ports':'light_ports',
                         'delay':'delay',
                         'timeout':'timeout',
                         'events_actions':'events_actions',
                         'sensor_type':'sensor_type'}
    
    SENSOR_CLOSE = False
    
    SENSOR_OPEN = True
    
    INVERT_PORT = 'INVERT_PORT'
    
    def __init__(self):
        """Este es un docstring antes de la funcion init """
        self.id = ""
        self.name = ""
        self.comment = ""
        self.sensors_ports = []
        self.device_ports = []
        
        self.sensor_type = self.SENSOR_CLOSE        
        
        self.events_actions = []
        
        self.regenerate_id()
    
    def regenerate_id(self):
        self.id = "LM_%d" % int(time.time()*10000000)
    
        
yaml.add_constructor(u'!DeviceMap',DeviceMap.yaml_constructor)
yaml.add_representer(DeviceMap, DeviceMap.yaml_representer)


