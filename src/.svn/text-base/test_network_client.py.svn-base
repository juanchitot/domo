#!/usr/bin/env python

# Echo client program

import sys
import zlib
import yaml
import errno
import socket
from telnetlib import Telnet

from network.net_msg import NetMsg
from interface.light_map import LightMap


def serialize():
    pass

def send_request(conection,data):
    try :
        conection.write(data)        
    except socket.error, e:
        if e.args[0] == errno.EPIPE :
            print "el socket esta cerrado"
            sys.exit()           
    
    try :
        print "leo de la conexion"
        r_data = conection.read_until("\n")        
    except:
        print "se produjo una excepcion en la lectura"
    
    compresed = r_data.rstrip("\n")
    compresed = compresed.decode("hex")
    yaml_coded = zlib.decompress(compresed)
    print yaml_coded

HOST = '192.168.1.12' # The remote host
PORT = 50007              # The same port as used by the server
try :
    conection = Telnet(HOST,PORT)
except Exception, e:
    print "No se pudo establecer la conexion %s " % e
    sys.exit()
conected = True
sock = conection.get_socket()
fd = sock.makefile()

while conected:
    if fd.closed :
        break
    comando = raw_input("ingrese el comando: ")
    if comando == 'ok' :
        l = LightMap()
        l.name="luces cocina"
        l.comment="comentraio sobre las luces de la cocina"        
        n = NetMsg()
        n.method='map_light'
        n.params=[l]
        n.status="conectado"
        encoded = zlib.compress(yaml.dump(n)).encode('hex')
        data = encoded + "\n"
        try :
            print  "escribio"
            conection.write(data)        
        except socket.error, e:
            if e.args[0] == errno.EPIPE :
                print "el socket esta cerrado"
                break           
    elif comando == 'get_in_ports':
        n = NetMsg()
        n.method='get_in_ports'
        n.params=[]
        n.status="conectado"
        encoded = zlib.compress(yaml.dump(n)).encode('hex')
        data = encoded + "\n"
        serialize()
        send_request(conection,data)
    
    elif comando == 'get_out_ports':
        n = NetMsg()
        n.method='get_out_ports'
        n.params=[]
        n.status="conectado"
        encoded = zlib.compress(yaml.dump(n)).encode('hex')
        data = encoded + "\n"
        serialize()
        send_request(conection,data)
    
    elif comando == 'error' :
        conection.write('adf\n')
    elif comando == 'disconect' :
        conected = False
        conection.write('')
    elif comando == 'shutdown' :
        conected = False
        n = NetMsg()
        n.method = 'shutdown'
        n.status = 'conectado'
        data = zlib.compress(yaml.dump(n)).encode('hex')+"\n"
        conection.write(data)
        
