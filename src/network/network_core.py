import time
import socket

import logging
import logger.domotica_logger

from network.domotica_tcp_server import DomoticaTcpServer
from network.network_exception import NetworkException

from core.control_core import ControlCore
from network.network_handler import TcpHandler

from threading import Thread

class NetworkCore:

    HOST = ''
    PORT = 50007
    
    network = None
    
    logger_instance = logging.getLogger('network.network_core')
    
    def __init__(self):
        self.running = False
        
        try:
            self.server = DomoticaTcpServer((self.HOST,self.PORT),TcpHandler)
        except socket.error:
            raise NetworkException(
"""Error: la direccion/puerto %s:%s esta en uso""" % (self.HOST,self.PORT))
    
    def get_instance():
        if NetworkCore.network == None:
            NetworkCore.network = NetworkCore()
        return NetworkCore.network  
    get_instance=staticmethod(get_instance)
    
    def initialize(self,domotica):
        self.core = domotica
        self.control = domotica.control
        self.server.control = self.control
        #         self.server_thread = Thread(target=self.server.serve_forever)
    
    def start(self):
        self.server.serve_forever()
    
    def shutdown(self):
        pass


        
if __name__ == '__main__' :    
    try:
        netcore = NetworkCore()
    except Exception, e:
        print e
    else:
        netcore.start()
