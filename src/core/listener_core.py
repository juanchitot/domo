from __future__ import with_statement
import os
from threading import Thread, Event, Lock
import time
import yaml
import logging

import sys

from Queue import Queue
from core.executer_core import ExecuterCore
from core.message import Message
from core.listener_core_exception import ListenerCoreException
from configurator.domotica_serialize import DomoticaSerialize

class ListenerCore(Thread,DomoticaSerialize):

    RealTimeCore = None
    logger_instance = logging.getLogger('domotica.real_time_core.listener_core')        
    high_priority_gate = Queue()
    normal_gate = Queue()
    
    serializable_data = {'listens_tail': 'listens_tail',
                         'listens': 'listens',
                         'in_ports': 'in_ports',
                         'out_ports': 'out_ports'}
 
    
    def __init__(self):
        Thread.__init__(self)        
        self.listens_tail = []
        self.listens = {}
        self.in_ports = {}
        self.out_ports = {}
        self.keep_running = True 
        self.have_self_lock = False
        ListenerCore.RealTimeCore = sys.modules['core.real_time_core'].RealTimeCore
    
    def add_event(self, event):
        self.logger_instance.debug("Agrego el evento %s" % event.get_event_id())
        event.load_involved_ports(self.in_ports,self.out_ports)
        self.listens[event.get_event_id()] = event
        self.listens_tail.append(event.get_event_id())
        
    def del_event(self, event_id):
        self.logger_instance.debug("Elimino el evento %s" % event_id )        
        if event_id in self.listens :
            del self.listens[event_id]
            self.listens_tail.remove(event_id)   
            if event_id in self.listens_tail:
                l_c_e = ListenerCoreException("El evento %s existe \
mas de una ves en el array listens_tail_remove" % event_id)

    def edit_event(self, event_id, event):
        if event_id in self.listens:
#             print "Hago un update del event"
            listened_event = self.listens[event_id]
            listened_event.edit(event)
            
    def publish_channel(self,channel,refresh_events=False):
        self.in_ports.update(channel.get_in_ports())
        self.out_ports.update(channel.get_out_ports())
#         print "listener publish channel"
#         print channel
#         self.print_ports_id()
#         self.logger_instance.debug("publico los puertos %s" % channel.get_in_ports().keys())
        if refresh_events :
            for event_id, event in self.listens.items():
                #               cl  print "------"
                #                 event.print_ports_id()
                event.load_involved_ports(self.in_ports,self.out_ports)
                event.print_ports_id()
    
    def print_ports_id(self):
        print "listener ports  -"
        st="ins\n"
        for p_k, p in  self.in_ports.items():
            st += " (%s,%d)" % (p_k,id(p))
        print st
        st = "outs\n"
        for p_k, p in  self.out_ports.items():
            st += " (%s,%d)" % (p_k,id(p))   
        print st
        print "========= "
    
    def run(self):
        while self.keep_running :
#             self.logger_instance.debug("while true del listener")
            self.process_high_priority_gate()
            self.process_normal_priority_gate()
            self.work()
    
    def process_high_priority_gate(self):
#         self.logger_instance.debug("process_high_priority_gate")
        while not ListenerCore.high_priority_gate.empty() :            
            msg = ListenerCore.high_priority_gate.get()
            self.logger_instance.debug("process_high_priority_gate ejecuta self.%s" % msg.method_name)
            if msg.method_name == 'stop' :
                try :
                    eval("self.%s()" % msg.method_name)
                except Exception, e:
                    d_e = DomoticaException(e)
                    d_e.log(ListenerCore.logger_instance)
                break
            elif msg.method_name == 'add_event' :                
                try :
                    self.add_event(msg.params[0])
                except Exception, e:
                    d_e = DomoticaException(e)
                    d_e.log(ListenerCore.logger_instance)
                    
            elif msg.method_name == 'publish_channel':
                self.publish_channel(msg.params[0],True)
            elif msg.method_name == 'del_event': 
                self.del_event(msg.params[0])
            elif msg.method_name == 'edit_event': 
                self.edit_event(msg.params[0],msg.params[1])
            else :
                raise ListenerCoreException("El metodo invocado no existe: %s" % msg.method_name)
    
    def process_normal_priority_gate(self):
        pass
    
    def work(self):
        RTCore = sys.modules['core.real_time_core'].RealTimeCore
#         print "realtimecoreclass in listener core"
#         print RTCore
        
        for event_id in self.listens_tail :
            event = self.listens[event_id]
            self.logger_instance.debug("Testeo el evento %s %s %s " % (event.get_event_id(),event.name,event.comment))
            if not event.enabled  or event.is_paused():
                continue
            if event.happend():                
                self.logger_instance.info("Sucedio el evento %s %s %s " % (event.get_event_id(),event.name,event.comment))
                RTCore.event_action_mapper_lock.acquire()
#                 print "id del rtcore %d" % id(sys.modules['core.real_time_core'].RealTimeCore)
                try:
                    action_id = RTCore.event_action_mapper[event_id]
                except Exception, e:
                    d_e = DomoticaException(e)
                    d_e.log(ListenerCore.logger_instance)
                RTCore.event_action_mapper_lock.release()                
                
                self.logger_instance.debug("envio la accion %s " % action_id)
                
                ExecuterCore.send_message(Message('fire_action',[action_id,event.get_params()]))                        
                if event.paused_mode :
                    self.logger_instance.debug("Pauso el  %s %s %s " % (event.get_event_id(),event.name,event.comment))
                    event.pause()
            
    
    def stop(self):
        raise SystemExit

    @classmethod    
    def yaml_constructor(cls,loader,node):        
#         print "entro al constructor de listener"
        [constructor_params,data_items] = loader.construct_sequence(node,True)        
        RTCore = sys.modules['core.real_time_core'].RealTimeCore.get_instance()        
#         print "id del RTCore %s " % id(RTCore)
#         print "listener yaml constructor"
#         print data_items
        setattr(RTCore.listener_core,'in_ports',data_items['in_ports'])
        setattr(RTCore.listener_core,'out_ports',data_items['out_ports'])
        
        for event_id, event in data_items['listens'].items():
            cls.logger_instance.info("Agrego el evento %s:%s " % (event_id,event.name))
            ListenerCore.add_event( RTCore.listener_core,event)      
        
        return RTCore.listener_core
    
    @classmethod
    def yaml_representer(cls,dumper,data):  
        for k in data.in_ports.keys():
            data.in_ports[k] = None
        for k in data.out_ports.keys():
            data.out_ports[k] = None
        
        return super(ListenerCore,cls).yaml_representer(dumper,data)

yaml.add_constructor(u'!ListenerCore',ListenerCore.yaml_constructor)
yaml.add_representer(ListenerCore, ListenerCore.yaml_representer)
