# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './templates/digital_card_status_template.ui'
#
# Created: Sun Jul 17 16:46:48 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(298, 501)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Frame.sizePolicy().hasHeightForWidth())
        Frame.setSizePolicy(sizePolicy)
        Frame.setAutoFillBackground(False)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Plain)
        Frame.setLineWidth(0)
        self.verticalLayout = QtGui.QVBoxLayout(Frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table_name = QtGui.QLabel(Frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_name.sizePolicy().hasHeightForWidth())
        self.table_name.setSizePolicy(sizePolicy)
        self.table_name.setScaledContents(True)
        self.table_name.setObjectName("table_name")
        self.verticalLayout.addWidget(self.table_name)
        self.ports_table = QtGui.QTableWidget(Frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ports_table.sizePolicy().hasHeightForWidth())
        self.ports_table.setSizePolicy(sizePolicy)
        self.ports_table.setStyleSheet("None")
        self.ports_table.setFrameShape(QtGui.QFrame.NoFrame)
        self.ports_table.setFrameShadow(QtGui.QFrame.Plain)
        self.ports_table.setLineWidth(0)
        self.ports_table.setAutoScroll(False)
        self.ports_table.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.ports_table.setShowGrid(True)
        self.ports_table.setGridStyle(QtCore.Qt.DotLine)
        self.ports_table.setWordWrap(True)
        self.ports_table.setObjectName("ports_table")
        self.ports_table.setColumnCount(2)
        self.ports_table.setRowCount(14)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setVerticalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.ports_table.setItem(0, 0, item)
        self.verticalLayout.addWidget(self.ports_table)

        self.retranslateUi(Frame)
        QtCore.QObject.connect(self.ports_table, QtCore.SIGNAL("cellClicked(int,int)"), Frame.change_port)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.table_name.setText(QtGui.QApplication.translate("Frame", "Digital Card", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(0).setText(QtGui.QApplication.translate("Frame", "Port_0", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(1).setText(QtGui.QApplication.translate("Frame", "Port_1", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(2).setText(QtGui.QApplication.translate("Frame", "Port_2", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(3).setText(QtGui.QApplication.translate("Frame", "Port_3", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(4).setText(QtGui.QApplication.translate("Frame", "Port_4", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(5).setText(QtGui.QApplication.translate("Frame", "Port_5", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(6).setText(QtGui.QApplication.translate("Frame", "Port_6", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(7).setText(QtGui.QApplication.translate("Frame", "Port_7", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(8).setText(QtGui.QApplication.translate("Frame", "Port_8", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(9).setText(QtGui.QApplication.translate("Frame", "Port_9", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(10).setText(QtGui.QApplication.translate("Frame", "Port_10", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(11).setText(QtGui.QApplication.translate("Frame", "Port_11", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(12).setText(QtGui.QApplication.translate("Frame", "Port_12", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.verticalHeaderItem(13).setText(QtGui.QApplication.translate("Frame", "Port_13", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Frame", "InPorts", None, QtGui.QApplication.UnicodeUTF8))
        self.ports_table.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Frame", "OutPorts", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.ports_table.isSortingEnabled()
        self.ports_table.setSortingEnabled(False)
        self.ports_table.setSortingEnabled(__sortingEnabled)
