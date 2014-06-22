import threading 

class ThreadClass(threading.Thread):
    
    def __init__(self,valor):
        threading.Thread.__init__(self)
        self.valor = valor
        self.terminar = 0
        self.suma  = 0
        
    def run(self):
        while not self.terminar:
            self.suma += 1 

    def terminar():
        self.terminar = 1
        
