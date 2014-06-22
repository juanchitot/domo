
class DomoticaSerialize:
    
    
    constructor_params = []
    serializable_data = {}
    
    @classmethod
#     - Dumpeo [parametros del constructor , data de la instancia]
#     - estos dos items son especificados en cada clase que 
#     la extiende como una secuencia y un diccionario
    def yaml_representer(cls,dumper,data):       
#         print "entro a yaml_representer con %s" % cls.__name__
        constructor_params = []
        props_hash = {}
        for param_name in data.constructor_params :            
            constructor_params.append(getattr(data,param_name))
            
        for prop, name in data.serializable_data.items():
#             if cls.__name__ == 'ListenerCore':
#                 print "en domotica serialize %s %s " % (prop,name)
#                 print repr(getattr(data,prop))
            props_hash[name] = getattr(data,prop)
        
#         if cls.__name__ == 'OutPort':
#             print "constructor_params y props "
#             print constructor_params
#             print props_hash
        return dumper.represent_sequence(u'!%s' % cls.__name__, [constructor_params,props_hash])
    
    @classmethod    
    def yaml_constructor(cls,loader,node):
        [constructor_params,data_items] = loader.construct_sequence(node,True)
        obj = cls(*constructor_params)
        for k,v in data_items.items():
            setattr(obj,k,v)
        return obj
