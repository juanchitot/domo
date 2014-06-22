from ui.home_map_item import HMItem
from ui.home_module import HomeModule

class HomeHeating(HomeModule):
    
    instance = None
        
    def work(self):
        for it_k, it in self.artifacts.items():
            port =  str((HMItem.ports(it,'In')[0]).toString())
            port_obj = self.client_core.in_ports[port]
            print port_obj
            it.setTemperature(port_obj.get_value())
    
