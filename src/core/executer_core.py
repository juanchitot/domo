import sys
import os
from threading import Thread, Event, Lock
from Queue import Queue
from executer_core_exception import ExecuterCoreException
import time
import yaml
import logging
from configurator.domotica_serialize import DomoticaSerialize


class ExecuterCore(Thread,DomoticaSerialize):   
    
    RealTimeCore = None
    logger_instance = logging.getLogger('domotica.real_time_core.executer_core')        
    high_priority_gate = Queue()
    normal_gate = Queue()
    no_work = Event()
    
    high_priority_message = ['publish_channel',
                             'stop',
                             'add_action',
                             'del_action']
    
    serializable_data = {'actions': 'actions',
                         'ports':'ports'}
    
    def __init__(self):
        Thread.__init__(self)
        self.ports={}
        self.actions = {}
        self.fired_actions = []
        self.receivers = {}
        self.keep_running = True
        self.have_self_lock = False
        ExecuterCore.RealTimeCore = sys.modules['core.real_time_core'].RealTimeCore
    
    def add_action(self,action):
        action.load_involved_ports(self.ports)
        self.actions[action.get_action_id()] = action

    def del_action(self,action_id):
        if action_id in self.actions:
            del self.actions[action_id]
#             print self.actions
    
    def add_receiver(self,receiver):
        self.receivers[receiver.get_receiver_id()] = receiver
        
    def fire_action(self,action_id,params={}):
        if action_id in self.actions.keys():                        
            self.actions[action_id].params = params
            if not  action_id in self.fired_actions:
#                 self.logger_instance.debug("agrego el action_id " )
                self.fired_actions.append(action_id)            
        else:
            e = ExecuterCoreException('La accion con id : %s no existe' % action_id )
            e.method = 'execute_action'
            e.params = params
            raise e
        
    def publish_channel(self,channel,refresh_actions=False):
#         print "executer publissh channel"
#         print channel
        self.ports.update(channel.get_out_ports())
        ExecuterCore.logger_instance.debug("publico los puertos %s" % channel.get_out_ports().keys())
        if refresh_actions :
            for action_id, action in self.actions.items():
#                 print "--------"
#                 action.print_ports_id()
                action.load_involved_ports(self.ports)
#                 action.print_ports_id()

        
    def run(self):
        while self.keep_running :
            self.no_work.clear() 
#             self.logger_instance.debug("while true del executer")
            self.process_high_priority_gate()
            self.process_normal_priority_gate()            
            self.work()
            self.no_work.wait()
            
    def process_high_priority_gate(self):
        
        while not ExecuterCore.high_priority_gate.empty() :            
            msg = ExecuterCore.high_priority_gate.get()
            self.logger_instance.debug("process_high_priority_gate ejecuta self.%s" % msg.method_name)
            if msg.method_name == 'stop' :
                eval("self.%s()" % msg.method_name)                
                break
            if msg.method_name == 'add_action' :
                try :
                    self.add_action(msg.params[0])
                except Exception, e:
                    d_e = DomoticaException(e)
                    d_e.log(self.logger_instance)
            if msg.method_name == 'publish_channel' :
                self.publish_channel(msg.params[0],True)
            if msg.method_name == 'del_action' :
                self.del_action(msg.params[0])
    
    def process_normal_priority_gate(self):
        
        while not ExecuterCore.normal_gate.empty() :            
            self.logger_instance.debug("normal_gate empty? %d " %  ExecuterCore.normal_gate.qsize())
            msg = ExecuterCore.normal_gate.get()
            self.logger_instance.debug("normal_gate ejecuta self.%s" % msg.method_name)
            if msg.method_name == 'fire_action' :
                self.fire_action(msg.params[0],msg.params[1])

    def work(self):
        self.logger_instance.debug("while work %d " % len( self.fired_actions ))
        while len( self.fired_actions ):
            action_id = self.fired_actions[0]
            action = self.actions[action_id]
            self.logger_instance.debug("Ejecuto la accion %s %s %s " % (action_id,action.name,action.comment))                               
#             action.print_ports_id()
            self.logger_instance.info("Ejecuto la accion %s:%s" % (action.get_action_id(),action.name))
            action.execute()
            del self.fired_actions[0]
                #del self.actions[action_id]
        
    def stop(self):
        raise SystemExit
        
    @classmethod
    def send_message(cls,message):
        if message.method_name in cls.high_priority_message:
            cls.high_priority_gate.put(message)            
        else:
            cls.normal_gate.put(message)            
        cls.no_work.set()

    @classmethod    
    def yaml_constructor(cls,loader,node):        
        [constructor_params,data_items] = loader.construct_sequence(node,True)
        RTCore = sys.modules['core.real_time_core'].RealTimeCore.get_instance()
#         print "id rtcoreexe %d id self %d" % (id(RTCore.executer_core),id(self))
        setattr(RTCore.executer_core,'ports',data_items['ports'])
#         print "add_action 
        for action_id, action in data_items['actions'].items():
            RTCore.executer_core.add_action(action)
        return RTCore.executer_core

yaml.add_constructor(u'!ExecuterCore',ExecuterCore.yaml_constructor)
yaml.add_representer(ExecuterCore, ExecuterCore.yaml_representer)
