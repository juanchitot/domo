from __future__ import with_statement
import logger.domotica_logger
import logging

from core.event.timer_event import TimerEvent
from core.event.boolean_event import BooleanEvent
from core.event.composite_event import CompositeEvent
from core.action.setter_action import SetterAction
from string import Template 

from threading import Thread, Lock
from core.message import Message
from core.listener_core import ListenerCore
from core.executer_core import ExecuterCore

from channel.bus import Bus
from channel.digital import Digital
from channel.channel_exception import ChannelException
from core.domotica_exception import DomoticaException
from datetime import timedelta
import yaml
import time
from configurator.domotica_serialize import DomoticaSerialize


class RealTimeCore(DomoticaSerialize):
    
    real_time_core = None
    logger_instance = logging.getLogger('domotica.real_time_core')
    event_action_mapper_lock = Lock()
    event_action_mapper = {}
    
    
    serializable_data = {'channels': 'channels',
                         'listener_core': 'listener_core',
                         'executer_core': 'executer_core',
                         'event_action_mapper': 'event_action_mapper'}

    
    def __init__(self):
        self.listener_core = ListenerCore()
        self.executer_core = ExecuterCore()
        self.channels = {}
        self.in_ports = {}
        self.out_ports = {}
        
    def get_instance():
        if RealTimeCore.real_time_core == None:
            RealTimeCore.logger_instance.debug("entro al if de get instance")
            RealTimeCore.real_time_core = RealTimeCore()            
        else: 
            RealTimeCore.logger_instance.debug("ya hay una instancia creada")
        return RealTimeCore.real_time_core    
    get_instance = staticmethod(get_instance)

    def initialize(self,domotica):
        pass
#         self.in_ports = self.listener_core.in_ports
#         self.out_ports = self.listener_core.in_ports
    
    def add_channel(self,channel,start=False):
        channel_id = channel.channel_id
        self.channels[ channel_id ] = channel
        self.logger_instance.debug("Agrego el channel %s" % channel_id)
        self.update_channel(channel_id)        
        if start :
            channel.start()            
            
    def update_channel(self,channel_id):
        channel = self.channels[ channel_id ]
        self.logger_instance.debug("Update del channel %s" % channel_id)                
        self.in_ports.update(channel.get_in_ports())        
        self.out_ports.update(channel.get_out_ports())
        ListenerCore.high_priority_gate.put(Message('publish_channel',[channel]))
        ExecuterCore.send_message(Message('publish_channel',[channel]))
    
    def start_channel(self,channel_id):
        if channel_id in self.channels:
            self.info("Enciendo el Channel %s" % channel_id)
            self.channels[channel_id].start()
    
    def stop_channel(self,channel_id):
        if channel_id in self.channels:
            self.channels[channel_id].stop()
            self.channels[channel_id].join()
    
    def start(self):
        self.start_channels()
        self.start_listener()
        self.start_executer()
    
    def start_listener(self):        
        self.listener_core.start()
        
    def start_executer(self):
        self.executer_core.start()
        
    def stop_listener(self):
        ListenerCore.high_priority_gate.put(Message('stop'))
        self.listener_core.join()
    
    def stop_executer(self):
        ExecuterCore.send_message(Message('stop'))
        self.executer_core.join()
    
    def stop_channels(self):
        for channel in self.channels.values():
            channel.stop()
            channel.join()
    
    def start_channels(self):
        for channel in self.channels.values():
            channel.test_cards_speeds()
            channel.start()
    
    def shutdown(self):
        self.stop_executer()
        self.stop_listener()
        self.stop_channels()
    
    def map_event(self,event,action):
        RealTimeCore.logger_instance.debug("Mapeo el evento %s:%s contra la accion %s:%s" % (event.get_event_id(),
                                                                                             event.name,
                                                                                             action.get_action_id(),
                                                                                             action.name))
        RealTimeCore.event_action_mapper_lock.acquire()
        RealTimeCore.event_action_mapper[event.get_event_id()] = action.get_action_id()
        RealTimeCore.event_action_mapper_lock.release()
        
        ListenerCore.high_priority_gate.put(Message('add_event',[event]))
        ExecuterCore.high_priority_gate.put(Message('add_action',[action]))
    
    def change_event(self,event):
        ListenerCore.high_priority_gate.put( Message('edit_event',[ event.event_id, event ]) )
        
    def unmap_event(self,event_id):
        
        RealTimeCore.event_action_mapper_lock.acquire()        
        action_id = RealTimeCore.event_action_mapper[event_id]
        del RealTimeCore.event_action_mapper[event_id]        
        RealTimeCore.event_action_mapper_lock.release()
        
        ListenerCore.high_priority_gate.put( Message('del_event',[event_id]) )
        ExecuterCore.send_message( Message('del_action',[action_id]) )
    
    @classmethod    
    def yaml_constructor(cls,loader,node):    
        [constructor_params,data_items] = loader.construct_sequence(node,True)
        RTCore = RealTimeCore.real_time_core
        
        for item,data in data_items.items():
            if item == 'channels':
                for c_n,c in data.items():
                    RTCore.add_channel(c,False)
            elif item == 'event_action_mapper':
                RealTimeCore.event_action_mapper = data
        return RTCore
    
yaml.add_constructor(u'!RealTimeCore',RealTimeCore.yaml_constructor)
yaml.add_representer(RealTimeCore, RealTimeCore.yaml_representer)
    
        



class TestRealTimeCore:
    
    def test(self):
        real_time_core = RealTimeCore.get_instance()
        #         Modo simulacion
        channel_0 = Bus(0,False)
#         channel_1 = Bus(1,True)
        
        channel_0.add_card(Digital(channel_0.channel_id,2))
        #        channel_0.add_card(2,'Digital')        
        #        channel_0.add_card(6,'Digital')        
        #         channel_0.add_card(16,'Digital')
        #         channel_0.add_card(33,'Analogic')
        #         channel_0.add_card(40,'Analogic')        
        #         channel_0.add_card(56,'Analogic')        
        #         channel_0.add_card(120,'Analogic')
        
        #        channel_1.add_card(0,'Digital')
        #        channel_1.add_card(2,'Digital')        
        #        channel_1.add_card(6,'Digital')        
        #         channel_1.add_card(16,'Digital')
        #         channel_1.add_card(33,'Analogic')
        #         channel_1.add_card(40,'Analogic')        
        #         channel_1.add_card(56,'Analogic')        
#         channel_1.add_card(120,'Analogic')
        channel_0.test_cards_speeds()
#         channel_1.test_cards_speeds()
        try : 
            real_time_core.add_channel(channel_0,True)
        except DomoticaException, e:
            e.log()
        
#         try : 
#             real_time_core.add_channel(channel_1,True)
#         except DomoticaException, e:
#             e.log()
        
        #cada 3 segundos y si hay movimiento prendo la luz        
            

            
#         procedimiento para vincular los sensores de movimiento 
#         y las luces
            
        boolean = BooleanEvent('Bus_0_I_02_00')
        boolean_2 = BooleanEvent('Bus_0_O_02_00',reverse=True)
        comp = CompositeEvent('%d and %d',[boolean,boolean_2],False)
        comp.name = 'Se detecto movimiento'     

        comp.pause_delta = timedelta(seconds=5)        
        comp.paused_mode = True

        #prendo este led    
        action = SetterAction(['Bus_0_O_02_00'],SetterAction.MODE_SET)        
        action.name = 'Prender luces'
        
        real_time_core.map_event(comp,action)
        
        
        boolean = BooleanEvent('Bus_0_I_02_00',reverse=True)
        timer = TimerEvent(None,timedelta(seconds=5),None)
        timer.name = 'Timer de 15 segundos sin movimiento'
        
        reset_condition = Template('not $%s' % boolean.get_event_id())
        comp = CompositeEvent('%d and %d',[boolean,timer],True,reset_condition)
        comp.name = 'Hace 15 segundos que no hay movimiento'
        
        out_ports = ['Bus_0_O_02_00']        
        action = SetterAction(out_ports,SetterAction.MODE_CLEAR)        
        action.name = 'Apagar luces'
         
        real_time_core.map_event(comp,action)
        
        #-------------------------------------------        

#         boolean = BooleanEvent('Bus_0_I_02_02',reverse=True)
#         timer.name = '';
        
#         reset_condition = Template('not $%s' % boolean.get_event_id())
#         comp = CompositeEvent('%d and %d',[boolean,timer],True,reset_condition)
#         comp.name = 'Hace 15 segundos que no hay movimiento'
        
#         out_ports = ['Bus_0_O_02_00']        
#         action = SetterAction(out_ports,SetterAction.MODE_CLEAR)        
#         action.name = 'Apagar luces'
        
#         real_time_core.map_event(comp,action)
        
        #-------------------------------------------        
        
        real_time_core.start_listener()
        real_time_core.start_executer()
        
        
        raw_input("Presiones una tecla para termiar el programa")
        #real_time_core.stop_channel(channel_0.channel_id)
        real_time_core.shutdown()

    def test_dump(self):
        real_time_core = RealTimeCore.get_instance()
        
        channel_0 = Bus(0,False)
        channel_1 = Bus(1,True)
        
        channel_0.add_card(Digital(channel_0.channel_id,2))
        channel_0.add_card(Digital(channel_0.channel_id,4))
        channel_0.add_card(Digital(channel_0.channel_id,6))
        
        channel_1.add_card(Digital(channel_1.channel_id,2))
        channel_1.add_card(Digital(channel_1.channel_id,2))
        channel_1.add_card(Digital(channel_1.channel_id,6))
        
        real_time_core.add_channel(channel_0,False)
        real_time_core.add_channel(channel_1,False)
#         -------------------------------------------------
        boolean = BooleanEvent('Bus_0_I_02_00')
        boolean_2 = BooleanEvent('Bus_0_O_02_00',reverse=True)
        comp = CompositeEvent('%d and %d',[boolean,boolean_2],False)
        comp.name = 'Se detecto movimiento'     
        
        comp.pause_delta = timedelta(seconds=5)        
        comp.paused_mode = True
        
        #prendo este led    
        action = SetterAction(['Bus_0_O_02_00'],SetterAction.MODE_SET)        
        action.name = 'Prender luces'
        real_time_core.map_event(comp,action)
#         -------------------------------------------------
        boolean = BooleanEvent('Bus_0_I_02_01')
        boolean_2 = BooleanEvent('Bus_0_O_02_01',reverse=True)
        comp = CompositeEvent('%d and %d',[boolean,boolean_2],False)
        comp.name = 'Se detecto movimiento'     
        
        comp.pause_delta = timedelta(seconds=5)        
        comp.paused_mode = True
        
        #prendo este led    
        action = SetterAction(['Bus_0_O_02_01'],SetterAction.MODE_SET)        
        action.name = 'Prender luces'
        real_time_core.map_event(comp,action)
#         -------------------------------------------------


        real_time_core.start_listener()
        real_time_core.start_executer()
        time.sleep(10)
        real_time_core.shutdown()
        
        print yaml.dump_all([real_time_core],explicit_start=True)
        
        
    def test_load(self):
        rep = """
--- !RealTimeCore
channels:
  Bus_0: !Bus
    bus_id: 0
    cards:
      2: !Digital {card_number: 2, channel_id: Bus_0}
      4: !Digital {card_number: 4, channel_id: Bus_0}
      6: !Digital {card_number: 6, channel_id: Bus_0}
    simulation_mode: false
  Bus_1: !Bus
    bus_id: 1
    cards:
      2: !Digital {card_number: 2, channel_id: Bus_1}
      6: !Digital {card_number: 6, channel_id: Bus_1}
    simulation_mode: true
"""
        r_t_c = yaml.load(rep)
        a=[1,2]
        print  yaml.dump_all([r_t_c,a],explicit_start=True)

if __name__ == '__main__' :    
    test = TestRealTimeCore()
    #     test.test()
    test.test_dump()
    test.test_load()
    



