from SocketServer import ThreadingTCPServer

class DomoticaTcpServer( ThreadingTCPServer ):
    
    def __init__(self,server_address, RequestHandlerClass):
        ThreadingTCPServer.__init__(self,server_address,RequestHandlerClass)
        self.control = None
        self.running = True
        
#     def serve_forever(self):
#         while self.running :
#             print "entro al while running"
#             self.handle_request()
    
#     def shutdown(self):
#         print "ejecuto un systemexit"
#         raise SystemExit
    
