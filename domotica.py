# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'domotica.ui'
#
# Created: Sat Oct 18 20:04:47 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    #esto es un comentario
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(683,537)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0,26,683,492))
        self.centralwidget.setObjectName("centralwidget")
        self.botton_sss = QtGui.QPushButton(self.centralwidget)
        self.botton_sss.setGeometry(QtCore.QRect(340,150,75,24))
        self.botton_sss.setObjectName("botton_sss")
        self.display_lcd = QtGui.QLCDNumber(self.centralwidget)
        self.display_lcd.setGeometry(QtCore.QRect(340,100,64,23))
        self.display_lcd.setObjectName("display_lcd")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,683,26))
        self.menubar.setObjectName("menubar")
        self.menuMain = QtGui.QMenu(self.menubar)
        self.menuMain.setObjectName("menuMain")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setGeometry(QtCore.QRect(0,518,683,19))
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionHola = QtGui.QAction(MainWindow)
        self.actionHola.setObjectName("actionHola")
        self.menuMain.addAction(self.actionHola)
        self.menubar.addAction(self.menuMain.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.botton_sss.setText(QtGui.QApplication.translate("MainWindow", "ssss", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMain.setTitle(QtGui.QApplication.translate("MainWindow", "main", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHola.setText(QtGui.QApplication.translate("MainWindow", "hola", None, QtGui.QApplication.UnicodeUTF8))

