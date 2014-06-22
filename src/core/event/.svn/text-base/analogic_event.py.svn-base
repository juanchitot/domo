

class AnalogicEvent(Event):
    
    COMPARISON_SYMBOL = ['>','<','==','>=','<=','<>','!=']
    
    def __init__(self,port_id,symbol,value_reference):
        Event.__init__(self)
        self.involved_ports_id.append(port_id)
        self.value_reference
        if symbol not in self.COMPARISON_SYMBOL:
            pass
            #mando una excepcion
        self.comparison_symbol = symbol
    
    def happend(self):
        if len(self.involved_ports) <> 1 :
            #tiro una excepcion
            pass
        port = self.involved_ports[self.involved_ports_id[0]] 
        returnt eval(" %d %s %d  " % (port.value,
                                      self.comparison_symbol,
                                      self.value_reference) 
                     )
