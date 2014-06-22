from __future__ import with_statement

import re
import sys
import os
import yaml


import traceback

from PyQt4.QtCore import QObject
from PyQt4 import QtCore
from core.singleton_core import SingletonCore
from ui.client_network_core import ClientNetworkCore

from ui.client_core_exception import ClientCoreException

from network.net_msg import NetMsg
from network.network_exception import NetworkException

from interface.light_map import LightMap

from threading import Lock

from datetime import datetime, timedelta

from configurator.domotica_configurator import DomoticaConfigurator
from configurator.configurator_exception import ConfiguratorException


class ClientCore(SingletonCore,QObject):
    instance = None
    
    STATUS_TIMEOUT = 20
    MAIN_CONFIG_FILE = 'ui/conf/domotica.conf'
    
    def __init__(self):
        QObject.__init__(self)

        self.net_core = ClientNetworkCore.get_instance()
        
        self.start_timer()
        self.clock_id = None
        
        self.in_ports = {}
        self.out_ports = {}
        
        self.channels = {}
        
        self.last_error = ''
        self.ports_loaded = False
        
        self.configurator = DomoticaConfigurator(self.MAIN_CONFIG_FILE)
        self.conf = {}
        self.load_configuration()
        
# Context manager
    def __enter__(self):
        self.stop_timer()
        self.emit(QtCore.SIGNAL('requestWaiting()'))
        return self
    
    def __exit__(self, e_type, e_value, e_tb):                
        self.start_timer()
        self.emit(QtCore.SIGNAL('requestArrived()'))
#         print "__exit__ client_Core"
        if e_type :
            if e_type == NetworkException :
#                 print "uno"
                self.last_error = str(e_value)
                self.reset_status()
                self.emit(QtCore.SIGNAL('connectionClosed()'))                
                return False
            if e_type == ClientCoreException:
#                 print "dos"
                self.last_error = str(e_value)
                return False
            else:
#                 print "tres"
                self.last_error = 'Se produjo un error inesperado'
                e = ClientCoreException(str(e_value),e_tb)
                self.last_error = str(e_value)
                self.emit(QtCore.SIGNAL('connectionClosed()'))
                raise e
            
# Fin context manager
    def connect(self):
        with self as manager :
            self.net_core.connect()
            self.start_timer()
            self.emit(QtCore.SIGNAL('connected()'))
# configuration
    def load_configuration(self):
        try :
            self.conf = self.configurator.load_configuration()
        except ConfiguratorException, e:
            print e
        else:
            net_module =  self.net_core.__class__.__name__
            if net_module in self.conf:
                self.net_core.load_configuration(self.conf[net_module])        
        
    def save_configuration(self):
        self.build_configuration()
        self.configurator.save_configuration(self.conf)
        
    def build_configuration(self):
        self.conf["%s" % self.net_core.__class__.__name__] = self.net_core.dump_configuration()
# end configuration    
    def get_domotica_server(self):
        return self.net_core.HOST
    
    def set_domotica_server(self,host):
        self.net_core.HOST = host
    
    def reset_status(self):
        self.stop_timer()
        self.in_ports.clear()
        self.out_ports.clear()
        self.channels.clear()
        self.ports_loaded = False
    
    def inform_status(self):
        # print "inform status"
        n = self.net_core.build_request_message('inform_status',
                                                [],
                                                'conectado')        
        with self as manager :
            self.net_core.request(n)            
            
    def add_light_map(self,lm):
        n = self.net_core.build_request_message('add_light_map',
                                                [lm],
                                                'conectado')        
        with self as manager :
            ret_net_msg = self.net_core.request(n)            
        
        self.emit(QtCore.SIGNAL('lightMapChange()'))
        return ret_net_msg.response
    
    def add_device_map(self,dm):
        n = self.net_core.build_request_message('add_device_map',
                                                [dm],
                                                'conectado')        
        with self as manager :
            ret_net_msg = self.net_core.request(n)            
        
            self.emit(QtCore.SIGNAL('DeviceMapperChange()'))
        return ret_net_msg.response
    
    def edit_light_map(self,lm):
        n = self.net_core.build_request_message('edit_light_map',
                                                [lm],
                                                'conectado')        
        with self as manager :
            ret_net_msg = self.net_core.request(n)            
        
        return ret_net_msg.response
    
    def del_light_map(self,lm):
        if isinstance(lm,list):
            lmps = lm
        else:
            lmps = [lm]
        n = self.net_core.build_request_message('del_light_map',
                                                lmps,
                                                'conectado')
        with self as manager:
            ret_net_msg = self.net_core.request(n)
            
        return ret_net_msg.response
    
    def get_light_maps(self):
        n = self.net_core.build_request_message('get_light_maps',
                                                [],
                                                'conectado')
        
        with self as manager :
            ret_net_msg = self.net_core.request(n)
            
        return ret_net_msg.response

    
    def timerEvent(self,event):
#         print "timer del client core"
#         print self.net_core.last_success_request
        if self.net_core.last_success_request < (datetime.now() - timedelta(seconds=self.STATUS_TIMEOUT)) :
#             print "ejecuto inform status"
            self.inform_status()
        self.ports_loaded = True
    
    def start_timer(self):
        if self.net_core.connected :      
            self.clock_id = self.startTimer(4000)
        
    def stop_timer(self):
        if self.clock_id :
            self.killTimer(self.clock_id)
    
    def set_ports(self,ports):        
        ports_param = {}
        for p_k in ports:
            if p_k in self.out_ports :
                ports_param[p_k] = self.out_ports[p_k]
            if p_k in self.in_ports :
                ports_param[p_k] = self.in_ports[p_k]
        
        n = self.net_core.build_request_message('set_ports',
                                                [ports_param],
                                                'conectado')
        
        with self as manager :
            ret_net_msg = self.net_core.request(n)
    
    def get_all_ports(self):
        n = self.net_core.build_request_message('get_all_ports',
                                                [],
                                                'conectado')
        
        with self as manager :
            ret_net_msg = self.net_core.request(n)
        
        response = ret_net_msg.response
#         print "entro a get all ports"
        
        r_e_i = r'Bus\_\d\_I\_\d{2}\_\d{2}' 
        for k, v in response.items():
            if re.match(r_e_i,k):
                self.in_ports[k] = v
#                 if re.match(r'Bus\_0\_I\_06\_\d{2}' , k):
#                     print "Port %s %s" % (k,v)
        
        r_e_o = r'Bus\_\d\_O\_\d{2}\_\d{2}' 
        for k,v in response.items():
            if  re.match(r_e_o, k):                
                self.out_ports[k] = v
#                 if re.match(r'Bus\_0\_O\_06\_\d{2}' , k):
#                     print "Port %s %s" % (k,v)
        
    
    def get_in_ports(self):
        n = self.net_core.build_request_message('get_in_ports',
                                                [],
                                                'conectado')
#         print "entro a get_in_ports"
        with self as manager :
            ret_net_msg = self.net_core.request(n)
            
        self.in_ports.update(ret_net_msg.response)
        return ret_net_msg.response
    
    def get_out_ports(self):
        n = self.net_core.build_request_message('get_out_ports',
                                                [],
                                                'conectado')
#         print "entro a get_in_ports"
        with self as manager :
            ret_net_msg = self.net_core.request(n)
            
        self.out_ports.update(ret_net_msg.response)
        return ret_net_msg.response
    
    def get_all_cards(self):
        n = self.net_core.build_request_message('get_cards',
                                                [],
                                                'conectado')
        with self as manager :
            ret_net_msg = self.net_core.request(n)
            
        self.channels.update(ret_net_msg.response)
    
    def get_analog_ports(self):
        self.get_all_ports()
        analog_cards = self.get_cards('Analogic')
        analog_ports = {}
#         print "entro a get_digital_in_ports"
        for k, c in analog_cards.items():
            
            bus_ch_dir = re.match(r'(Bus)\_(\d)\_(\d{2})', k ).groups()
            r_e = r'%s\_%s\_I\_%s\_\d{2}' %  bus_ch_dir
            
            for p_k in self.in_ports.keys():
                if re.match(r_e, p_k):
                    analog_ports[p_k] = self.in_ports[p_k]
        
        return analog_ports
    
    def get_digital_in_ports(self):
        self.get_all_ports()
        dig_cards = self.get_cards('Digital')
        in_dig_ports = {}
#         print "entro a get_digital_in_ports"
        for dc_k, dc in dig_cards.items():
            
            bus_ch_dir = re.match(r'(Bus)\_(\d)\_(\d{2})', dc_k ).groups()
            r_e = r'%s\_%s\_I\_%s\_\d{2}' %  bus_ch_dir
            
            for p_k in self.in_ports.keys():
                if re.match(r_e, p_k):
                    in_dig_ports[p_k] = self.in_ports[p_k]
                    
        return in_dig_ports
    
    def get_digital_out_ports(self):
        dig_cards = self.get_cards('Digital')
        out_dig_ports = {}
        
        for dc_k, dc in dig_cards.items():
            
            bus_ch_dir = re.match(r'(Bus)\_(\d)\_(\d{2})', dc_k ).groups()
            r_e = r'%s\_%s\_O\_%s\_\d{2}' %  bus_ch_dir
            
            for p_k in self.out_ports.keys():
                if re.match(r_e, p_k):
                    out_dig_ports[p_k ] = self.out_ports[p_k]
                    
        return out_dig_ports
    
    
    def get_cards(self,type=None):
        self.get_all_cards()
        cards = {}
        for ch_name, ch in self.channels.items():
            for c_id, c in ch.items():
                if type :
                    if c['type'] == type  :
                        cards[ c['card_id'] ] = c
                else:
                    cards[ c['card_id'] ] = c
        return cards

    def remove_card(self,card_id):
        print "remuevo la targeta %s " % card_id
    
    def add_card(self,card_dir,bus_dir,type):
        params = [card_dir,bus_dir,type]
        n = self.net_core.build_request_message('add_card',
                                                params,                                
                                                'conectado')
        
        with self as manager :
            ret_msg = manager.net_core.request(n)
#             print "printeo ret_msg %s" % ret_msg
            if ret_msg.error_code :
                e = ClientCoreException(ret_msg.error_msg)
                raise e
        
        self.get_all_ports()
        self.emit(QtCore.SIGNAL('cardsAdded()'))
        
    def search_connected_cards(self,channel_id):
        params = [channel_id]
        n = self.net_core.build_request_message('search_connected_cards',
                                                params,                                
                                                'conectado')
        with self as manager :
            ret_msg = self.net_core.request(n)                        
            return ret_msg.response        
        
