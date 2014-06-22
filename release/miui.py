
from PyQt4 import QtCore, QtGui
from  Ui_Domotica import Ui_Form
import  sys
from card.bus import Bus


class Formulario(QtGui.QWidget,Ui_Form):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.setupUi(self)
        self.__bus = Bus(0)
        self.__bus.add_card('00','Digital')
#       self.__bus.add_card('16','Analogic')
        self.timer = QtCore.QTimer(self)
        QtCore.QObject.connect(self.timer,QtCore.SIGNAL('timeout()'), self.synchronize_ui)
        self.timer.start(500)
        
    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.timer.stop()
            self.close()
        
    
    def mi_eslot1(self):
        self.lcd_2.display('1')
        
        
    def synchronize_ui(self):
        self.__dict__['clock_lcd'].display(QtCore.QTime.currentTime().toString('hh:mm:ss AP'))
        self.__bus.read_cards()
        dig_card = self.__bus.get_card('00')
        for i in range(14):

            in_port_i = dig_card.__getattr__("port_in_%d" % i)
            in_check_i = self.__dict__['in_%d' % i]
            in_check_i.setChecked(bool(in_port_i))
            
            out_check_i = self.__dict__['out_%d' % i]            
            dig_card.__setattr__('port_%d' % i,int(out_check_i.isChecked()))
#             print "el check_in %d  esta en %d " % (i,int(in_check_i.isChecked()))
#             print "el check_out %d  esta en %d " % (i,int(out_check_i.isChecked()))            
#             print dig_card
        self.__bus.flush_cards()
        
#        analog_card = self.__bus.get_card('16')
#        for i in range(9):
#            read_val = analog_card.__getattr__('port_in_%d' % i)
#             read_val = read_val * 1.97
#            (self.__dict__['analogic_in_%d' % i]).display(read_val)
            
        
        
        
        
app = QtGui.QApplication(sys.argv)
f = Formulario()
f.show()
app.exec_()

