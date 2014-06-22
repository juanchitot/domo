#!/usr/bin/env python

import SocketServer
import socket
import sys 
import zlib
import time
HOST = '192.168.1.12'
PORT = 50007

class TcpHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        f = open("domotica_logging.log")
        print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        r = f.read(1024*1024*10)
        while len(r):
            data=zlib.compress(r)
            #             print "crc = %d" % zlib.crc32(data)
            self.wfile.write(data.encode('hex')+"\n" )
            r = f.read(1024)
        print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

server = SocketServer.TCPServer((HOST,PORT),TcpHandler)
server.handle_request()
server.socket.close()
