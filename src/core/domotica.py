import yaml
import sys
import time
import signal

import logger.domotica_logger
import logging

from core.real_time_core import RealTimeCore
from core.control_core import ControlCore
from network.network_core import NetworkCore

from configurator.domotica_configurator import DomoticaConfigurator
from configurator.configurator_exception import ConfiguratorException

from channel.bus import Bus
from channel.digital import Digital

from core.event.timer_event import TimerEvent
from core.event.boolean_event import BooleanEvent
from core.event.composite_event import CompositeEvent

from core.action.setter_action import SetterAction

from string import Template 

from datetime import timedelta

from core.domotica_exception import DomoticaException

class Domotica:
    
    MAIN_CONFIG_FILE = 'conf/domotica.conf'
    
    logger_instance = logging.getLogger('domotica')
    save_data = []
    
    def __init__(self):
        self.initialized = False
        self.RTCore = RealTimeCore.get_instance()
        self.rt_core = self.RTCore
        self.save_data.append(self.rt_core)
        
        self.conf = DomoticaConfigurator(self.MAIN_CONFIG_FILE) 
        
        self.control = ControlCore.get_instance()
        self.save_data.append(self.control)
        
        self.network = NetworkCore.get_instance()

    
    def initialize(self):
        signal.signal(signal.SIGUSR1,self.signal_handler)
        
        self.logger_instance.info('Domotica, inicializa RealTimeCore')
        self.rt_core.initialize(self)
        
        self.logger_instance.info('Domotica, inicializa Configurator')
        self.conf.initialize(self)
        
        self.logger_instance.info('Domotica, inicializa ControlCore')
        self.control.initialize(self)
        
        self.logger_instance.info('Domotica, inicializa NetworkCore')
        self.network.initialize(self)
        
        self.initialized = True
        
    def start(self):
        if not self.initialized:
            raise DomoticaException("""No se inicializaron los cores.
Llamar al metodo initialize()
""")
        try :
            self.conf.load_configuration()
        except ConfiguratorException, e:
            self.logger_instance.info('Domotica, inicia sin cargar configuracion')
            self.logger_instance.debug("Error al cargar la configuracion %s" % repr(e))
            
        self.rt_core.start()
        try :
            self.network.start()
        except KeyboardInterrupt:
            self.shutdown()

    
    def shutdown(self):
#         print "entro a shutdown"
        self.logger_instance.info('Domotica, El sistema se apagara')
        self.logger_instance.info('Domotica, guardando configuracion')
        self.conf.save_configuration(self.save_data)
        self.logger_instance.info('Domotica, RealTimeCore shutdown')
        self.rt_core.shutdown()
        self.logger_instance.info('Domotica, NetworkCore shutdown')
        self.network.shutdown()
        self.logger_instance.info('Domotica Shutdown')
        
    def signal_handler(self,signum,frame):
        self.shutdown()
        sys.exit()
        
                
def test_control():
    d = Domotica()
    d.initialize()
    d.start()
    
    
def test_save():
    d = Domotica()
    #         Modo simulacion
    channel_0 = Bus(0,False)
    
    channel_0.add_card(Digital(channel_0.channel_id,2))
    channel_0.test_cards_speeds()
    
    try : 
        d.RTCore.add_channel(channel_0,True)
    except DomoticaException, e:
        e.log()
                
        boolean = BooleanEvent(None,'Bus_0_I_02_01')
        boolean_2 = BooleanEvent(None,'Bus_0_O_02_01',reverse=True)
        comp = CompositeEvent(None,'%d and %d',[boolean,boolean_2],None,False)
        comp.name = 'Se detecto movimiento'     
        
        comp.pause_delta = timedelta(seconds=5)        
        comp.paused_mode = True
        
        #prendo este led    
        action = SetterAction(None,['Bus_0_O_02_01'],SetterAction.MODE_SET)        
        action.name = 'Prender luces'
        
        d.RTCore.map_event(comp,action)
        
        
        boolean = BooleanEvent(None,'Bus_0_I_02_01',reverse=True)
        timer = TimerEvent(None,None,timedelta(seconds=5),None)
        timer.name = 'Timer de 15 segundos sin movimiento'
        
        reset_condition = Template('not $%s' % boolean.get_event_id())
        comp = CompositeEvent(None,'%d and %d',[boolean,timer],True,reset_condition)
        comp.name = 'Hace 15 segundos que no hay movimiento'
        
        out_ports = ['Bus_0_O_02_01']        
        action = SetterAction(None,out_ports,SetterAction.MODE_CLEAR)        
        action.name = 'Apagar luces'
        
        d.RTCore.map_event(comp,action)
        
        d.RTCore.start_executer()
        time.sleep(2)
        d.RTCore.start_listener()
        
        
        
        raw_input("Presiones una tecla para termiar el programa")
        #real_time_core.stop_channel(channel_0.channel_id)
        d.RTCore.shutdown()
        try:
            d.conf.save_configuration(d.RTCore)
        except ConfiguratorException, e:
            e.log(self.logger_instance)
#         print yaml.dump(d.RTCore)
        

    def test_load():
        d = Domotica()
        d.conf.load_configuration()

        d.RTCore.start_listener()
        d.RTCore.start_executer()
        d.RTCore.start_channels()
        
        raw_input("Presiones una tecla para termiar el programa")
        d.RTCore.shutdown()
#         print yaml.dump(d.RTCore)

    def test_load_2():
        d = Domotica()
        d.conf.load_configuration()

        d.RTCore.start_listener()
        d.RTCore.start_executer()
        d.RTCore.start_channels()
        
        time.sleep(2)
# raw_input("Presiones una tecla para continuar el programa")

        boolean = BooleanEvent(None,'Bus_0_I_02_02')
        boolean_2 = BooleanEvent(None,'Bus_0_O_02_02',reverse=True)
        comp = CompositeEvent(None,'%d and %d',[boolean,boolean_2],None,False)
        comp.name = 'Se detecto movimiento luz 1'     
        
        comp.pause_delta = timedelta(seconds=5)        
        comp.paused_mode = True
        
        #prendo este led    
        action = SetterAction(None,['Bus_0_O_02_02'],SetterAction.MODE_SET)        
        action.name = 'Prender luces luz 1'
        
        d.RTCore.map_event(comp,action)
        
        
        boolean = BooleanEvent(None,'Bus_0_I_02_02',reverse=True)
        timer = TimerEvent(None,None,timedelta(seconds=5),None)
        timer.name = 'Timer de 15 segundos sin movimiento luz 1'
        
        reset_condition = Template('not $%s' % boolean.get_event_id())
        comp = CompositeEvent(None,'%d and %d',[boolean,timer],True,reset_condition)
        comp.name = 'Hace 15 segundos que no hay movimiento luz 1'
        
        out_ports = ['Bus_0_O_02_02']        
        action = SetterAction(None,out_ports,SetterAction.MODE_CLEAR)        
        action.name = 'Apagar luces 1'
        
        d.RTCore.map_event(comp,action)
        
        raw_input("Presiones una tecla para terminar el programa")

        d.RTCore.shutdown()
#         print yaml.dump(d.RTCore)


if __name__ == '__main__' :            
    if len(sys.argv)>1:
        if sys.argv[1] == 'load':
            test_load_2()
        elif sys.argv[1] == 'save':
            test_save()
        elif sys.argv[1] == 'control':
            test_control()
