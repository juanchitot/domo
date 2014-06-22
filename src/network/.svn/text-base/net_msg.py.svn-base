import yaml
from configurator.domotica_serialize import DomoticaSerialize
class NetMsg(DomoticaSerialize):
    
    serializable_data = {'method':'method',
                         'params':'params',
                         'status':'status',
                         'data':'data',
                         'response':'response',
                         'error_code': 'error_code',
                         'error_msg': 'error_msg'}
    
    def __init__(self):
        self.method = ''
        self.params = []
        self.status = None
        self.data = '' 
        self.response = ''
        self.error_code = 0
        self.error_msg = ''

yaml.add_constructor(u'!NetMsg',NetMsg.yaml_constructor)
yaml.add_representer(NetMsg, NetMsg.yaml_representer)
