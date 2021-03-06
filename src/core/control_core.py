import yaml
import string
import logger.domotica_logger
import logging
import re

from network.net_msg import NetMsg
# import sys
# import time

from core.real_time_core import RealTimeCore
# from configurator.domotica_configurator import DomoticaConfigurator
# from configurator.configurator_exception import ConfiguratorException

from threading import Lock

from channel.channel_exception import ChannelException
from channel.bus import Bus
from channel.digital import Digital
from channel.analogic import Analogic
from channel.debug import DebugCard

from core.event.boolean_event import BooleanEvent
from core.event.composite_event import CompositeEvent
from core.action.setter_action import SetterAction
from core.event.timer_event import TimerEvent
from string import Template 

from datetime import timedelta
from core.control_core_exception import ControlCoreException
from configurator.domotica_serialize import DomoticaSerialize

class ControlCore(DomoticaSerialize):
    
    control = None    
    logger_instance = logging.getLogger('domotica.control_core')
    lock = Lock()    
    map_objects = {}
    light_map_re = re.compile('LM\_\d+')
    
    serializable_data = {'map_objects': 'map_objects'}
    
    
    def get_instance():
        if ControlCore.control == None:
            ControlCore.control = ControlCore()
        return ControlCore.control
    get_instance=staticmethod(get_instance)
    
    def initialize(self,domotica):
        self.core = domotica
        self.rt_core = domotica.rt_core
        
    def get_exported_methods(self):
        #{'method_name':'num_params'}
        exported_methods = {'shutdown':0,
                            'inform_status':0,
                            'search_connected_cards':1,
                            'set_ports':1,
                            'get_all_ports':0,
                            'get_in_ports':0,
                            'get_out_ports':0,
                            'get_analog_ports':0,
                            'add_light_map':1,
                            'del_light_map':1,
                            'edit_light_map':1,
                            'get_cards':0,
                            'add_card':3,
                            'remove_card':2,
                            'get_light_maps':0}        
        return exported_methods
    
    def shutdown(self,net_msg):
        self.core.network.shutdown()
    
    def inform_status(self,net_msg):
        ret_msg = NetMsg()
        ret_msg.response = ''
        ret_msg.error_code = 0
        return ret_msg        
    
    def search_connected_cards(self,net_msg):
        channel_number = net_msg.params[0]        
        channel_id = "Bus_%s" % channel_number
        
        ret_msg = NetMsg()
        ret_msg.response = ''
        ret_msg.error_code = 0
        
        paused = False
#         print self.rt_core.channels
        if channel_id in self.rt_core.channels:
#             print "el channel esta"
            channel = self.rt_core.channels[channel_id]
            if not channel.paused :
                channel.pause()
#                 print "pauso el channel"
                paused = True
        
        ret_msg.response = Bus.search_connected_cards(channel_number)
#         print "retorno \n%s"% ret_msg.response
        
        if paused : channel.resume()
        
        return ret_msg
    
    
    def get_cards(self,net_msg):
        cards_tree = {}
        for ch_name, ch in self.rt_core.channels.items():
            ch_cards = {}
            
            for c_name, c in  ch.cards.items():
                ch_cards[c_name] = {'simulation_mode': c.simulation_mode , 
                                    'card_id': c.card_id, 
                                    'channel_id': c.channel_id,
                                    'type': c.type()}
                
            cards_tree[ch_name] = ch_cards
        ret_msg = NetMsg()
        ret_msg.response = cards_tree
        return ret_msg
    
    def get_all_ports(self,net_msg):
        ret_msg = NetMsg()
        ret_msg.response = {}
        ret_msg.response.update(self.rt_core.in_ports)
        ret_msg.response.update(self.rt_core.out_ports)
        return ret_msg
    
    def get_in_ports(self,net_msg):
        ret_msg = NetMsg()
#         print yaml.dump(self.rt_core.in_ports)
        ret_msg.response = self.rt_core.in_ports
        return ret_msg


    def get_out_ports(self,net_msg):
        ret_msg = NetMsg()
        ret_msg.response = self.rt_core.out_ports
#         print yaml.dump(self.rt_core.in_ports)
        return ret_msg
    
    def get_analog_ports(self,net_msg):
        pass
    
    def get_light_maps(self,net_msg):
        ret_msg = NetMsg()
        ret_msg.response = {}
#         print "entro a get_light_maps"
#         print yaml.dump(self.map_objects)
        for m_id, m in self.map_objects.items():
#             print "entro a get_light_maps"
            if self.light_map_re.match(m_id) :
                ret_msg.response[m_id] = m
        
        return ret_msg
    
#   - !LightMap
#     - []
#     - {comment: aaaaaaaaa, 
#        light_ports: {Bus_0_O_02_00:true}, 
#        name: sssss, 
#        delay: 0, 
#        timeout: 0,
#       sensors_ports: {Bus_0_I_02_00:false}}
    
    def add_light_map(self,net_msg):
        lm = net_msg.params[0]
        try :
            maps = lm.build_map_objects()
        except Exception, e:
            d_e = DomoticaException(e)
            d_e.log(self.logger_instance)
            print e
        
        self.rt_core.map_event(maps[0][0],maps[0][1])
        lm.events_actions.append([maps[0][0].get_event_id(),
                                  maps[0][1].get_action_id()])
        
        self.rt_core.map_event(maps[1][0],maps[1][1])
        lm.events_actions.append([maps[1][0].get_event_id(),
                                  maps[1][1].get_action_id()])
        
        lm.regenerate_id()
        self.map_objects[lm.id] = lm
        
        net_msg_ret = NetMsg()
        net_msg_ret.response = lm
        return net_msg_ret
    
    def set_ports(self,net_msg):
        ret_msg = NetMsg()
        
        missing_ports = []
        
        ports = net_msg.params[0]
        for p_k, p in ports.items():
            if p_k in self.rt_core.out_ports:
                self.rt_core.out_ports[p_k].set_value(p.get_value())
                print "%s %d %s" % (p_k,
                                    id(self.rt_core.out_ports[p_k]),
                                    self.rt_core.out_ports[p_k])
            if p_k in self.rt_core.in_ports:
                self.rt_core.in_ports[p_k].set_value(p.get_value())
                print "%s %d %s" % (p_k,
                                    id(self.rt_core.in_ports[p_k]),
                                    self.rt_core.in_ports[p_k])
            else:
                missing_ports.append(p_k)
                
        if not len(missing_ports):
            ret_msg.response = 'Se seteo el puerto OK'
            ret_msg.error_code = 0
        else:
            ret_msg.error_code = -1
            ret_msg.error_msg = "Se produjeron errores al setear \
los puertos %s" % string.join( missing_ports,',') 
        return ret_msg
    
    def edit_light_map(self,net_msg):
        lm = net_msg.params[0]
        try :
            maps = lm.build_map_objects()
        except Exception, e:
            d_e = DomoticaException(e)
            d_e.log(self.logger_instance)
            print e        
            
        old_lmp = self.map_objects[lm.id]        
        old_lmp.delay = lm.delay
        old_lmp.timeout = lm.timeout
        old_lmp.name = lm.name
        old_lmp.comment = lm.comment
        
        move_event_id =  old_lmp.events_actions[0][0]        
        no_move_event_id =  old_lmp.events_actions[1][0]
        
        maps[0][0].event_id = move_event_id
        maps[1][0].event_id = no_move_event_id
        self.rt_core.change_event(maps[0][0])
        self.rt_core.change_event(maps[1][0])
                
        ret_msg = NetMsg()
        ret_msg.error_code = 0        
        return ret_msg
    
            
    def del_light_map(self,net_msg):
#         print "entro a del_light_map"
        lm = net_msg.params[0]
        maped_lm = self.map_objects[lm.id]
        for ev_ac in maped_lm.events_actions:
            ev_id = ev_ac[0]
            self.rt_core.unmap_event(ev_id)        
            
        del self.map_objects[lm.id]
        ret_msg = NetMsg()
        ret_msg.error_code = 0        
        return ret_msg
    
#     parametros: card_direction,card_type,bus_id
    def add_card(self,net_msg):        
        c_dir = net_msg.params[0]
        b_dir = net_msg.params[1]
        type = net_msg.params[2]
        
        ret_msg = NetMsg()
        channels = self.rt_core.channels
        ch_key = "Bus_%d" % b_dir        
        
        if not type in Bus.supported_card_types:
            ret_msg.error_code = -1
            ret_msg.error_msg = 'El tipo de targeta %s no existe ' % type
            return ret_msg
        
        if not ch_key in channels:
            try :
                ch = Bus(b_dir,True)
            except ChannelException, e:                    
                e.log(self.logger_instance)
                
                ret_msg.error_code = -1
                ret_msg.error_msg = 'Error: el canal %d no pudo ser creado' % b_dir
                return ret_msg            
            
            self.rt_core.add_channel(ch,False) 
            ch.start()
        else :
            ch = channels[ch_key]
            
        if  c_dir in channels[ch_key].cards :
            ret_msg.error_code = -1
            ret_msg.error_msg = 'Error: la placa que desea agregar ya existe'
            return ret_msg                        
        
        ch.pause()
        try :
            if type == 'Digital' :
                ch.add_card( Digital(ch.channel_id,c_dir) )
            elif type == 'Analogic' :
                ch.add_card( Analogic(ch.channel_id,c_dir) )
            else:
                ch.add_card( DebugCard(ch.channel_id,c_dir) ) 
            
        except Exception, e:
            cce=ControlCoreException("No se pudo agregar la placa con \
direccion %s al bus %s, excepcion %s " % (c_dir,ch.channel_id,e.message))
            cce.log(self.logger_instance)
            
            ch.resume()
            
            ret_msg.error_code = -1
            ret_msg.error_msg = cce.message
            return ret_msg
        
        ch.test_cards_speeds(c_dir)
#         print yaml.dump(ch.cards)
        
        if not ch.cards[c_dir].timeout_cote :
            
            ch.remove_card(c_dir)
            ch.resume()
            
            ret_msg.error_code = -1
            ret_msg.error_msg = 'Como la placa no repondio en ninguno\
 de los tests de velocidad no fue agregada'
            return ret_msg
        
        ch.resume()
        self.rt_core.update_channel(ch.channel_id)
        
        ret_msg.error_code = 0
        ret_msg.response = 'La targeta con direccion %s fue agregada' % c_dir
        return ret_msg
    
    #parametros: card_direction,bus_id
    def remove_card(self,net_msg):        
        c_dir = net_msg.params[0]
        b_dir = net_msg.params[1]
        
        print "Elimino la targeta %s " % c_dir
        
        ret_msg = NetMsg()
        ret_msg.error_code = 0
        ret_msg.response = 'La targeta con direccion %s fue removida' % c_dir
        return ret_msg
        
        
    
    
    @classmethod    
    def yaml_constructor(cls,loader,node):    
#         print "id del control core %s " % id(ControlCore.control)
        [constructor_params,data_items] = loader.construct_sequence(node,True)
        control_core = ControlCore.get_instance()
#         print "id del control_core %s " % id(control_core)        
        for k,v in data_items.items():
#             print "seteo %s en el control core" % k
#             print v
            setattr(control_core,k,v)
        return control_core

yaml.add_constructor(u'!ControlCore',ControlCore.yaml_constructor)
yaml.add_representer(ControlCore, ControlCore.yaml_representer)
