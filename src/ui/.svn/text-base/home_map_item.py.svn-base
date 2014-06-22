from core.domotica_exception import StaticClassException

from PyQt4.QtCore import QVariant as V
   

class HMItem:
    
    ITEM_MODULE = 1    
    ITEM_NAME = 10
    ITEM_TYPE = 20
    ITEM_SELECTION_STATE = 30
    ITEM_LEVEL = 40
    ITEM_IN_PORTS = 50
    ITEM_OUT_PORTS = 60

    #items types
    OUTLINE_POINT = 'OUTLINE POINT'
    SELECTION_POINT = 'SELECTION POINT'
    MAP = 'MAP'
    MAP_AREA = 'MAP AREA'
    ARTIFACT = 'ARTIFACT'
    
    def __init__(self):
        raise StaticClassException('La clase %s es estatica y no \
puede ser instanciada' % self.__class__.__name__)
    @classmethod
    def repr(cls,item):
        print "mod: %s, name: %s, type: %s, selec: %s, level: %s" % (HMItem.module(item),
                                                                     HMItem.name(item),
                                                                     HMItem.type(item),
                                                                     HMItem.select(item),
                                                                     HMItem.level(item))
    
    @classmethod
    def module(cls,item,module=None):
        if module is None :
            v = item.data(cls.ITEM_MODULE)
            if v.isValid():
                return v.toString()
            return None
        else :
            item.setData(cls.ITEM_MODULE,V(module))

    @classmethod
    def name(cls,item,name=None):
        if name is None :
            v = item.data(cls.ITEM_NAME)
            if v.isValid():
                return v.toString()
            return None            
        else :
            item.setData(cls.ITEM_NAME,V(name))
    
    @classmethod
    def type(cls,item,type=None):
        if type is None :
            v = item.data(cls.ITEM_TYPE)
            if v.isValid():
                return v.toString()
            return None
        else :
            item.setData(cls.ITEM_TYPE,V(type))
            
    @classmethod
    def select(cls,item,state=None):
        if state is None :
            v = item.data(cls.ITEM_SELECTION_STATE)
            if v.isValid():
                return v.toBool()
            return None
        else :
            item.setData(cls.ITEM_SELECTION_STATE,V(state))
    
    @classmethod
    def level(cls,item,level=None):
        if level is None :
            v = item.data(cls.ITEM_LEVEL)
            if v.isValid():
                return v.toInt()[0]
            return None
        else :
            item.setData(cls.ITEM_LEVEL,V(level))

    @classmethod
    def ports(cls,item,type='In',ports=[]):
        if not len(ports) :
            if type == 'In':
                return item.data(cls.ITEM_IN_PORTS).toList()
            else: # 'Out'
                return item.data(cls.ITEM_OUT_PORTS).toList()
        else:
            if type == 'In':
                item.setData(cls.ITEM_IN_PORTS,V(ports))
            else:
                item.setData(cls.ITEM_OUT_PORTS,V(ports))
                    
    @classmethod
    def cmp(cls,item_a,item_b):
        ret = []
        if not cls.module(item_a) == None:
            ret.append(cls.module(item_a) == cls.module(item_b))
        if not cls.name(item_a) == None:
            ret.append(cls.name(item_a) == cls.name(item_b))
        if not cls.type(item_a) == None:
            ret.append(cls.type(item_a) == cls.type(item_b))
        if not cls.select(item_a) == None:
            ret.append(cls.select(item_a) == cls.select(item_b))
        if not cls.level(item_a) == None:
            ret.append(cls.level(item_a) == cls.level(item_b))
        
        if len(ret):
            print ""
            HMItem.repr(item_a)
            HMItem.repr(item_b)
            print ret
            return False not in ret
        return False
    
    @classmethod
    def equal(cls,item_a,item_b):
        return cls.module(item_a) == cls.module(item_b) and \
            cls.module(item_a) == cls.module(item_b) and \
            cls.name(item_a) == cls.name(item_b) and \
            cls.type(item_a) == cls.type(item_b) and \
            cls.select(item_a) == cls.select(item_b) and \
            cls.level(item_a) == cls.level(item_b)
    
    
