#!/usr/bin/env python


from PyQt4.QtCore import QObject,QEvent

class Test:
    
    instance = None
    
    def __init__(self):
        self.prop = 'hola'
#         if Test.instance is None:
#             self.property = 'hola'
#             Test.instance = self
#         else:
#             return Test.instance
        
    @classmethod
    def getInstance(cls):
        return cls.instance
    
    
class Test2(Test):
    
    def __init__(self):
        Test.__init__(self)
        self.prop2 = 'chau'
    
    def __getattr__(self,name):
        if name == 'prop':
            return "holasddd"


t = Test()
print "prop %s " %  t.prop
t2 = Test2()
print "prop %s " %  t2.prop
print "prop2 %s " %  t2.prop2
# a = {'a':1,'b':2}
# print 1 in a
 
# t = Test()
# o = QObject()


# instancemethod = type(t.func)

# o.cal = instancemethod(Test2.set_call,o,Test)
# print o.cal
# print o
# o.cal()

# print "%s" % Test2.cal
# print "%s" % t.func
# print "%s" % Test.func
# t.cal = Test2.cal
# print "%s" % t.cal
# t2 = Test2()
# print QEvent.Type.
# if hasattr(t2,'set_call'):
#     print type(type( getattr(t2,'set_call')).__name__)
#     print getattr(t2,'set_call')


