from ui.home_module import HomeModule

class AdminHomeModule(HomeModule):
    
    @classmethod
    def initialize( cls, parent_cls, instance):
        instance.home_module = parent_cls.get_instance()
        print "home_heating_module %s " % id(instance.home_module)
    
    # QEvent.GraphicsSceneMousePress
    def event_handler_156(self,obj,event):
        return super(AdminHomeModule,self).event_handler_156(obj,event)
        
    #QEvent.GraphicsSceneMouseRelease
    def event_handler_157(self,obj,event):
        return super(AdminHomeModule,self).event_handler_157(obj,event)
        
