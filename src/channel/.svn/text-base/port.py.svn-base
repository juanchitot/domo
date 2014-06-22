import yaml
from configurator.domotica_serialize import DomoticaSerialize
# TODO: 
# - Hacer que channel_id,device_id y port_number sean 
# valores solo lectura


class Port(object,DomoticaSerialize):

    __slots__ = ['channel_id','device_number','port_number','port_id','value']

    constructor_params = ['channel_id','device_number','port_number','value']

    def __init__(self,channel_id,device_number,port_number,value=None):
        self.port_id = "%s_%02d_%02d" % (channel_id,device_number,port_number)
        self.channel_id = channel_id
        self.device_number = device_number
        self.port_number = port_number
        self.value = value
    
    def get_id(self):
        return self.port_id
    
    def set_value(self,value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "Port : %s , value : %d " % (self.port_id,self.value)
    
    
    
class InPort(Port):
    
    def __init__(self,channel_id,device_number,port_number,value=None):
        
        Port.__init__(self,channel_id,device_number,port_number,value)
        self.port_id = "%s_I_%02d_%02d" % (channel_id,device_number,port_number)        

yaml.add_constructor(u'!InPort',InPort.yaml_constructor)
yaml.add_representer(InPort, InPort.yaml_representer)
    

class OutPort(Port):

    def __init__(self,channel_id,device_number,port_number,value=None):        
        Port.__init__(self,channel_id,device_number,port_number,value)
        self.port_id = "%s_O_%02d_%02d" % (channel_id,device_number,port_number)        

yaml.add_constructor(u'!OutPort',OutPort.yaml_constructor)
yaml.add_representer(OutPort, OutPort.yaml_representer)




class TestPort:

    def run(self):
        Iport = InPort(0,1,0,0)
        Oport = OutPort(0,1,0,0)
        pass
        
    

if __name__ == '__main__' :
    
    test = TestPort()
    test.run()
