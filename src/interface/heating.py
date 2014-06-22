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


class Heating(DomoticaSerialize):
    
#     serializable_data = {'id' : 'id',
#                          'name':'name',
#                          'comment':'comment',
#                          'sensors_ports':'sensors_ports',
#                          'light_ports':'light_ports',
#                          'delay':'delay',
#                          'timeout':'timeout',
#                          'events_actions':'events_actions',
#                          'sensor_type':'sensor_type'}
    
