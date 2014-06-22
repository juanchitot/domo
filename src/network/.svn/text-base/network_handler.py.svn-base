import time
import zlib
import yaml
import socket

from SocketServer import StreamRequestHandler

from network.network_exception import NetworkException
from network.net_msg import NetMsg

from interface.light_map import LightMap

import logging
import logger.domotica_logger

from datetime import datetime,timedelta

class TcpHandler(StreamRequestHandler):
     
     logger_instance = logging.getLogger('network.network_handler')
     
     READ_ERRORS_LIMIT = 2
     WRITE_ERRORS_LIMIT = 6
     REQUEST_ERRORS_LIMIT = 6
     CHECK_ERRORS_INTERVAL = timedelta(seconds=60)
     CONNECTION_TIMEOUT = 30 
     
     def __init__(self, request, client_address, server): 
          self.connection_time = datetime.today()
          self.last_connection_check = datetime.today()
          self.in_data = None
          self.out_data = None
          self.control = server.control
          self.read_errors = 0
          self.write_errors = 0
          self.request_errors = 0
          self.client_full_address = "%s:%s" % (client_address[0], 
                                                client_address[1]) 
          StreamRequestHandler.__init__(self, request, client_address, server)
     
     def handle(self):
          self.request.settimeout(self.CONNECTION_TIMEOUT)
          self.disconnect = False
          while not self.disconnect :               
               try :
                    self.read_data()
               except KeyboardInterrupt, e:
                    raise e
               except socket.timeout, e:
                    self.read_errors += 1
                    self.logger_instance.error("""Se produjo un timeout al leer el socket %s """ % e)         
               except Exception, e :
                    self.read_errors += 1
                    self.logger_instance.error("""Se produjo una excepcion al leer del socket %s """ % e)
               if self.read_errors > self.READ_ERRORS_LIMIT :
                    self.disconnect = True
                    self.logger_instance.error("""Se produjeron demasiados errores de lectura seguidos (%d) se desconecta al cliente %s""" % 
                                               (self.read_errors, self.client_full_address) )         
               
               if self.in_data :
                    try :
                         self.handle_call()
                    except KeyboardInterrupt, e:
                         raise e
                    except Exception, e:
                         self.request_errors += 1
                         self.logger_instance.error("""Se produjo un error al procesar un pedido 
del cliente %s, Excepcion: %s""" % ( self.client_full_address, str(e) ) )         
                    else:
                         self.in_data = None
                    if self.request_errors > self.REQUEST_ERRORS_LIMIT :
                         self.disconnect = True
                         self.logger_instance.error("""Se produjeron demasiados errores en los pedidos(%d) seguidos se desconecta al cliente %s""" % 
                                                    (self.request_errors, self.client_full_address ) )
               
                    
                    if self.out_data:
                         try :
                              self.write_data()
                         except KeyboardInterrupt, e:
                              raise e
                         except Exception, e:
                              self.write_errors += 1
                              self.logger_instance.error("""Se produjo un error al escribir 
datos al cliente %s, Excepcion: %s""" % ( self.client_full_address , str(e) ) )         
                         if self.write_errors > self.WRITE_ERRORS_LIMIT :
                              self.disconnect = True
                              self.logger_instance.error("""Se produjeron demasiados errores de escritura(%d) seguidos
se desconecta al cliente %s""" % (self.write_errors, self.client_full_address ) )
                         else:
                              self.out_data = None
                         
     def read_data(self):
          self.raw_data = self.rfile.readline()
          if len(self.raw_data):
               self.timeout = 0
               compresed = self.raw_data.rstrip("\n")
               compresed = compresed.decode("hex")
               yaml_coded = zlib.decompress(compresed)
               self.in_data = yaml.load(yaml_coded)
               self.read_errors = 0
          else:
               self.disconnect = True
     
     def write_data(self):
          yaml_coded = yaml.dump(self.out_data)
          compressed = zlib.compress(yaml_coded)
          compressed = compressed.encode('hex') 
          raw_data = compressed + '\n'
          self.wfile.write(raw_data)
          self.write_errors = 0
     
     def handle_call(self):
          self.out_data = True # None
          net_msg = self.in_data
          
          exp_methods = self.control.get_exported_methods()
          
          if net_msg.method in exp_methods :
               method_params = exp_methods[ net_msg.method ]
               if len(net_msg.params) != method_params :
                    self.logger_instance.error(
                         "Error: cliente %s, metodo %s, params count (%d,%d)" % (self.client_full_address,
                                                                                 net_msg.method,
                                                                                 method_params,
                                                                                 len(net_msg.params))
                         )
                    
                    res_msg = NetMsg()
                    res_msg.error_core = -1
                    res_msg.error_msg = 'Cantidad de parametros invalida, (%d != %d)' % (
                         method_params,
                         len(net_msg.params))                    
                    
                    self.out_data = res_msg
               
               self.logger_instance.debug("El cliente %s llamo al metodo %s" % (self.client_full_address,net_msg.method))
               f = eval("self.control.%s" % net_msg.method )
               self.out_data=f(net_msg)
          else:
               res_msg = NetMsg()
               res_msg.error_code = -1
               res_msg.error_msg = 'Nombre de metodo invalido (%s)' % net_msg.method
               self.out_data = res_msg
               self.logger_instance.error(
                    "Error: cliente %s, el metodo %s no existe" % (self.client_full_address,
                                                                   net_msg.method )
                    )
                 
               
          self.request_errors = 0
