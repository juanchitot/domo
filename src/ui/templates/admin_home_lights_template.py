# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './templates/admin_home_lights_template.ui'
#
# Created: Sun Jul 17 16:46:48 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        Form.resize(745, 767)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 2)
        self.label = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.level_combo = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.level_combo.sizePolicy().hasHeightForWidth())
        self.level_combo.setSizePolicy(sizePolicy)
        self.level_combo.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.level_combo.setObjectName("level_combo")
        self.gridLayout.addWidget(self.level_combo, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)
        self.home_map_view = QtGui.QGraphicsView(Form)
        self.home_map_view.setMinimumSize(QtCore.QSize(400, 300))
        self.home_map_view.setObjectName("home_map_view")
        self.gridLayout.addWidget(self.home_map_view, 0, 2, 6, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Floor:", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
