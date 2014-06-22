import sys
import zlib
import yaml
import errno
import socket

from channel.port import InPort,OutPort

from PyQt4.QtCore import QObject, QCoreApplication, QEventLoop
from core.singleton_core import SingletonCore

from telnetlib import Telnet

from network.net_msg import NetMsg

from network.network_exception import NetworkException
from threading import Event, Thread, Lock
from datetime import datetime, timedelta

class ClientNetworkCore(SingletonCore,QObject):
    instance = None
    
    THREADED_REQUESTS = False
    
    waiting_response = Event()
    threaded_response = None
    
    def __init__(self):
        QObject.__init__(self)
        
        self.HOST = 'localhost'
        self.PORT = 50007
        
        self.status = 'DESCONECTADO'
        self.connected = False
        self.last_success_request = (datetime.now() - timedelta(hours=1))
    
    def dump_configuration(self):
        return {'HOST': self.HOST,
                'PORT': self.PORT}
    def load_configuration(self,conf):
        if 'HOST' in conf:
            self.HOST = conf['HOST']                        
        if 'PORT' in conf:
            self.PORT = conf['PORT']
    
#     def timerEvent(self,event):
#         print "sucedio el evento en el client network core"
        
#     def start_timer(self):
#         self.clock_id = self.startTimer(1000)
        
#     def stop_timer(self):
#         self.killTimer(self.clock_id)
    
    def connect(self):
        try :
            self.conection = Telnet(self.HOST,self.PORT)
            self.sock = self.conection.get_socket()
            self.fd = self.sock.makefile()
            
            self.status = 'CONECTADO'
            self.connected = True
        except Exception, e:
            new_e = NetworkException( "No se pudo establecer la \
conexion con el server.\n Cheque que la direccion sea correcta o el server este encendido")
            new_e.log_level_msg = e.message
            raise new_e

    def request(self, net_msg):
        if not self.THREADED_REQUESTS :            
            ret = self.no_threaded_request(net_msg)
            self.last_success_request = datetime.now()
            return ret
        else:
            #             print "inicio thread"
            request_thread = Thread(target=self.threaded_request,args=[net_msg])
            
            self.waiting_response.clear()
            
            request_thread.start()
            
            while not self.waiting_response.isSet():
                pass
                # QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
            
            ret = self.__class__.threaded_response
            self.__class__.threaded_response = None
            
            if isinstance(ret, Exception):
                raise ret 
            else :                
                self.last_success_request = datetime.now()
                return ret
    
    def threaded_request(self, net_msg):
        try :
            self.__class__.threaded_response = self.no_threaded_request(net_msg)
#             print "thread request salio ok"
        except Exception, e:
#             print "thread request salio con error"
            self.__class__.threaded_response = e
        
        self.waiting_response.set()
            
    def no_threaded_request(self,net_msg):
        if not self.connected :
            raise NetworkException( "El cliente no se encuentra connectado")            
        
        data = self.serialize(net_msg)
        try :
            self.conection.write(data)        
        except socket.error, e:
            if e.args[0] == errno.EPIPE :                
                self.connected = False
                new_e = NetworkException( "Error: se produjo una desconexion mientras se enviaban datos")
                new_e.log_level_msg = e.message
                raise new_e
        except Exception, e:
            new_e = NetworkException( "Error: se produjo un error inesperado cuando enviaban datos al server")
            new_e.log_level_msg = e.message
            raise new_e
        
        try :        
            r_data = self.conection.read_until("\n")        
        except Exception, e:
            new_e = NetworkException( "Error: se produjo una desconexion mientras se leian datos")
            new_e.log_level_msg = e.message
            raise new_e
        
        ret_net_msg = self.deserialize(r_data)
        return ret_net_msg
            
    def serialize(self,net_msg):
        encoded = zlib.compress(yaml.dump(net_msg)).encode('hex')
        data = encoded + "\n"
        return data
    
    def deserialize(self,stream):
        compresed = stream.rstrip("\n")
        compresed = compresed.decode("hex")
        yaml_coded = zlib.decompress(compresed)
        data = yaml.load(yaml_coded)
        return data
    
    
    def build_request_message(self, method, params, status):
        n = NetMsg()
        n.method = method
        n.params = params
        n.status = status
        return n
        
