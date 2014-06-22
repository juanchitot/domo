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



class LightMap(DomoticaSerialize):
    
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
        self.light_ports = []
        self.sensor_type = self.SENSOR_CLOSE
        self.timeout = None
        self.delay = None
        self.events_actions = []
        
        self.regenerate_id()
    
    def regenerate_id(self):
        self.id = "LM_%d" % int(time.time()*10000000)
    
    def build_map_objects(self): 
        map_one = self.if_move_lights_on()
        map_two = self.if_no_move_lights_off()
#         print yaml.dump(map_one)
#         print yaml.dump(map_two)
        return  (map_one,map_two)
    
    def edit(self, lmp):
        print "edit de light_map"
        #composite event
        try:
            move_on = self.events_actions[0][0]
        #este es el evento que maneja el delay
            move_on_t_e = move_on.events[1]
            move_on_t_e.from_start = lmp.delay
        #cambio el pause_delta con el timeout
            move_on.pause_delta = lmp.timeout/2
        
            no_move = self.events_actions[1][0]
        
            no_move_time = no_move.events[1]
            no_move_time.from_start = lmp.timeout
        except Exception,e:
            print e
        print "salgo de edit"
        return (move_on, no_move)
        
    
    def if_move_lights_on(self):
        # un boolean event por sensor
        sensors_events = []
        for sensor, type in self.sensors_ports.items():
            if type == self.SENSOR_CLOSE:
                rev = False
            else :
                rev = True
            # el evento es true cuando el circuito esta cerrado
            b_e = BooleanEvent(None, sensor, reverse=rev)
            b_e.name = "sensor_%s_revert_(%d)" %(sensor,b_e.reverse)
            sensors_events.append(b_e)
        
        # un boolean event por luz
        lights_events = []
        for light, type in self.light_ports.items():
            if type == self.INVERT_PORT:
                rev = True
            else:
                rev = False
                
            rev = not rev
            # el event es true cuando el circuito esta abierto(luz no activa)
            b_e = BooleanEvent(None, light,reverse=rev)
            b_e.name = "luz_%s_revert_(%d)" % (light,b_e.reverse)
            lights_events.append(b_e)
            
        # algun sensor detecto movimiento
        sensors_or = string.join(['%d'] * len(sensors_events),
                                 ' or ')
        # alguna luz esta apagada
        lights_or = string.join(['%d'] * len(lights_events),
                                ' or ')
        
        move_and_no_light = CompositeEvent(None,
                                           '(%s) and (%s)' % (sensors_or,lights_or),
                                           sensors_events+lights_events,
                                           None,
                                           False)
        move_and_no_light.name = 'Se detecto movimiento'             

        # cuento "timeout" segundos desde que no hay movimiento y disparo
        delay_time = TimerEvent(None,None,self.delay,None)
        delay_time.name = 'Timer de %s delay si hay movimiento' % self.delay
        
        #cuando NO hay movimiento reseteo el timer
        reset_condition = Template('not $%s' % move_and_no_light.get_event_id())
        
        move_and_no_light_delay = CompositeEvent(None,
                                                 '%d and %d',
                                                 [move_and_no_light,delay_time],
                                                 True,
                                                 reset_condition)
        move_and_no_light_delay.name = 'Se detecto movimiento hace %s tiempo' % self.delay      
        move_and_no_light_delay.pause_delta = self.timeout/2
        move_and_no_light_delay.paused_mode = True        
        
        on_lights = SetterAction(None,self.light_ports,SetterAction.MODE_SET)        
        on_lights.name = 'Prender luces'
        
        return (move_and_no_light_delay,on_lights)
    
    def if_no_move_lights_off(self):
        
        # un boolean event por sensor
        sensors_events = []
        for sensor, type in self.sensors_ports.items():
            if type == self.SENSOR_CLOSE:
                rev = False
            else :
                rev = True
            # el evento es true cuando el circuito esta abierto
            # osea que no hay movimiento
            rev = not rev
            b_e = BooleanEvent(None, sensor, reverse=rev)
            b_e.name = "sensor_%s_revert_(%d)" %(sensor,b_e.reverse)
            sensors_events.append(b_e)
            
        # and de sensores de movimiento
        sensors_and = string.join(['%d'] * len(sensors_events),
                                  ' and ')
        #ningun sensor detecta movimiento
        move_off = CompositeEvent(None,
                                  sensors_and,
                                  sensors_events,
                                  False,
                                  False)
                
        #cuento "timeout" segundos desde que no hay movimiento y disparo
        no_move_time = TimerEvent(None,None,self.timeout,None)
        no_move_time.name = 'Timer de %s sin movimiento' % self.timeout
        
        #cuando hay movimiento reseteo el timer
        reset_condition = Template('not $%s' % move_off.get_event_id())
        
        time_without_move = CompositeEvent(None,
                                           '%d and %d',
                                           [move_off,no_move_time],
                                           True,
                                           reset_condition)
        time_without_move.name = 'Hace 15 segundos que no hay movimiento'
        

        
        off_lights = SetterAction(None,self.light_ports,SetterAction.MODE_CLEAR)        
        off_lights.name = 'Apagar luces'
        
        return (time_without_move,off_lights)
        
yaml.add_constructor(u'!LightMap',LightMap.yaml_constructor)
yaml.add_representer(LightMap, LightMap.yaml_representer)


