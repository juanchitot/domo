# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './templates/floating_window_template.ui'
#
# Created: Sun Jul 17 16:46:48 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.setWindowModality(QtCore.Qt.WindowModal)
        DockWidget.resize(400, 432)
        DockWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        DockWidget.setStyleSheet("None")
        DockWidget.setFloating(True)
        DockWidget.setFeatures(QtGui.QDockWidget.DockWidgetClosable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.close_button = QtGui.QPushButton(self.dockWidgetContents)
        self.close_button.setObjectName("close_button")
        self.gridLayout.addWidget(self.close_button, 6, 2, 1, 1)
        self.connect_button = QtGui.QPushButton(self.dockWidgetContents)
        self.connect_button.setObjectName("connect_button")
        self.gridLayout.addWidget(self.connect_button, 6, 1, 1, 1)
        self.msg_text = QtGui.QLabel(self.dockWidgetContents)
        self.msg_text.setObjectName("msg_text")
        self.gridLayout.addWidget(self.msg_text, 1, 1, 1, 2)
        self.domotica_host = QtGui.QLineEdit(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.domotica_host.sizePolicy().hasHeightForWidth())
        self.domotica_host.setSizePolicy(sizePolicy)
        self.domotica_host.setObjectName("domotica_host")
        self.gridLayout.addWidget(self.domotica_host, 3, 1, 1, 2)
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 4)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 4, 0, 1, 4)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 2, 0, 1, 4)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 3, 3, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QObject.connect(self.domotica_host, QtCore.SIGNAL("returnPressed()"), self.connect_button.click)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(QtGui.QApplication.translate("DockWidget", "Domotica", None, QtGui.QApplication.UnicodeUTF8))
        self.close_button.setText(QtGui.QApplication.translate("DockWidget", "Cerrar", None, QtGui.QApplication.UnicodeUTF8))
        self.connect_button.setText(QtGui.QApplication.translate("DockWidget", "Conectar", None, QtGui.QApplication.UnicodeUTF8))
        self.msg_text.setText(QtGui.QApplication.translate("DockWidget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DockWidget", "Domotica Host", None, QtGui.QApplication.UnicodeUTF8))

