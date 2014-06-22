from PyQt4.QtGui import QGraphicsTextItem

class TemperatureItem(QGraphicsTextItem):
    
    DISPLAY_TEMPLATE =  '''
<strong >
%0.1f &deg; &nbsp; Grados
</strong>
'''    
    def __init__ (self,parent=None,scene=None):
        QGraphicsTextItem.__init__(self,parent,scene)
    
    def setTemperature(self,temp):
        self.setHtml(TemperatureItem.DISPLAY_TEMPLATE % temp)
