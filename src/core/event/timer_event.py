import yaml
from core.event.event import Event
from datetime import datetime 
from datetime import timedelta 


class TimerEvent(Event):

    constructor_params = ['event_id','start','from_start','every']
    
    def __init__(self,event_id,start=None,from_start=None,every=None):
        Event.__init__(self,event_id)
        if not event_id:            
            self.event_id = 'TE_%d' % self.event_id

#         - la marca de comienzo del evento es el start_mark
#         que si no se pasa como parametro es datetime.now()
#         - el evento empieza a dispararse luego de concurrido 
#         el timedelta from_start o inmediatamente en caso de ser 
#         este nulo.
#         - una vez que el evento se dispara, se volvera a disparar
#         cada fire_every timedelta en caso de ese no ser nulo
#         - last_fire es usado para indicar la hora del ultimo suceso
#         del evento, en caso de todabia no haberse ejecutado es nulo
        
        if not start :
            start = datetime.now()

        if not from_start :
            from_start = timedelta()

        if not every :
            every = timedelta()
        
        self.start_mark = start
        self.start = start

        self.from_start = from_start
        self.fire_every = every
        self.every = every
        self.last_fire = None
        
        self.initialized = True    
    
    
    def happend(self):
        now = datetime.now()
#         print "happend timer event"
#         print self.start_mark
#         print self.from_start
#         print now
#         print (self.start_mark+self.from_start)
#         print self.last_fire
#         print "---"
        if self.is_paused() :
            return False        

        if (self.start_mark+self.from_start) > now :
            #falta para que se empieze a disparar el evento
            return False
        #el evento se podria a empezar a disparar
        if self.fire_every :
            #el evento debe dispararse cada un deltatime
            if  not self.last_fire or ( self.fire_every + self.last_fire ) <= now :
                #no se ejecuto nunca o paso delta time desde la ultima vez que se disparo
                self.last_fire = now
                return True
        
        if not self.last_fire :            
            #el evento ya se puede disparar y no se disparo nunca
            self.last_fire = now
            return True
        
        #el evento ya se disparo
        return False
    
    def get_params(self):
        self.params['last_fired'] = self.last_fire
        return self.params
    
    def reset(self):
        self.start_mark = datetime.now()
        self.last_fire = None
        
    def edit(self,event):
        if not isinstance(event,TimerEvent):
            raise EventException("TimerEvent.edit(%s), \
event no es un TimerEvent" % self.event_id)
        self.start_mark = event.start_mark
        self.start = event.start
        self.from_start = event.from_start
        self.fire_every = event.fire_every

yaml.add_constructor(u'!TimerEvent',TimerEvent.yaml_constructor)
yaml.add_representer(TimerEvent, TimerEvent.yaml_representer)
