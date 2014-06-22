#!/usr/bin/python  -dv

import sys


from PyQt4 import QtCore, QtGui

from PyQt4.QtGui import QApplication, \
    QStyleFactory

from PyQt4.QtCore import QTranslator

from ui.domotica_client import DomoticaClient

from ui.admin_home_map import AdminHomeMap




app = QtGui.QApplication(sys.argv)
QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
# QApplication.setStyle(QStyleFactory.create('plastique'))


trs = ['es','us']
def_tr = 'us'

for i in range(len(sys.argv)):
    v = sys.argv[i]
    if v in ('-lang','--lang'):
        if (i < len(sys.argv)-1):
            v = sys.argv[i+1]
            if v in trs:
                def_tr = v

tr = QTranslator()
tr.load('domotica_%s' % def_tr ,'ui/translations')
app.installTranslator(tr)


main_window = QtGui.QMainWindow()
main_window.setCentralWidget(DomoticaClient(main_window))
main_window.show()
app.exec_()
