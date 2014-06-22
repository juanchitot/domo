class SingletonCore:
        
    @classmethod
    def get_instance(cls,*args):
        if cls.instance == None:
#             print "creo un singleton de %s" % cls.__name__
            if len(args):
                cls.instance = cls(*args)
            else:
                cls.instance = cls()
        return cls.instance
    
class Singleton(SingletonCore):
    pass
