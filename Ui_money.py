# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\E3\Code測試區\pythonTest\money\money.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1059, 760)
        Dialog.setSizeGripEnabled(True)
        self.push_save = QtWidgets.QPushButton(Dialog)
        self.push_save.setGeometry(QtCore.QRect(190, 270, 93, 28))
        self.push_save.setObjectName("push_save")
        self.input_cost = QtWidgets.QLineEdit(Dialog)
        self.input_cost.setGeometry(QtCore.QRect(180, 80, 113, 22))
        self.input_cost.setObjectName("input_cost")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 80, 91, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 140, 91, 21))
        self.label_2.setObjectName("label_2")
        self.input_item = QtWidgets.QLineEdit(Dialog)
        self.input_item.setGeometry(QtCore.QRect(180, 140, 113, 22))
        self.input_item.setObjectName("input_item")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 200, 91, 21))
        self.label_3.setObjectName("label_3")
        self.push_plot = QtWidgets.QPushButton(Dialog)
        self.push_plot.setGeometry(QtCore.QRect(580, 160, 93, 28))
        self.push_plot.setObjectName("push_plot")
        self.input_date = QtWidgets.QLineEdit(Dialog)
        self.input_date.setGeometry(QtCore.QRect(180, 200, 113, 22))
        self.input_date.setObjectName("input_date")
        self.label_cost = QtWidgets.QLabel(Dialog)
        self.label_cost.setGeometry(QtCore.QRect(340, 80, 58, 15))
        self.label_cost.setObjectName("label_cost")
        self.push_close = QtWidgets.QPushButton(Dialog)
        self.push_close.setGeometry(QtCore.QRect(190, 380, 93, 28))
        self.push_close.setObjectName("push_close")
        self.plot_date = QtWidgets.QPushButton(Dialog)
        self.plot_date.setGeometry(QtCore.QRect(580, 240, 93, 28))
        self.plot_date.setObjectName("plot_date")
        self.push_origin = QtWidgets.QPushButton(Dialog)
        self.push_origin.setGeometry(QtCore.QRect(580, 80, 93, 28))
        self.push_origin.setObjectName("push_origin")
        self.calendarWidget = QtWidgets.QCalendarWidget(Dialog)
        self.calendarWidget.setGeometry(QtCore.QRect(470, 400, 296, 229))
        self.calendarWidget.setObjectName("calendarWidget")
        self.push_average = QtWidgets.QPushButton(Dialog)
        self.push_average.setGeometry(QtCore.QRect(200, 520, 93, 28))
        self.push_average.setObjectName("push_average")
        self.label_average = QtWidgets.QLabel(Dialog)
        self.label_average.setGeometry(QtCore.QRect(210, 580, 121, 16))
        self.label_average.setObjectName("label_average")
        self.input_month = QtWidgets.QLineEdit(Dialog)
        self.input_month.setGeometry(QtCore.QRect(700, 240, 113, 22))
        self.input_month.setObjectName("input_month")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(820, 240, 58, 15))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        self.push_close.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.push_save.setText(_translate("Dialog", "儲存"))
        self.label.setText(_translate("Dialog", "輸入消費金額"))
        self.label_2.setText(_translate("Dialog", "輸入消費項目"))
        self.label_3.setText(_translate("Dialog", "輸入消費時間"))
        self.push_plot.setText(_translate("Dialog", "作圖"))
        self.label_cost.setText(_translate("Dialog", "金額"))
        self.push_close.setText(_translate("Dialog", "關閉"))
        self.plot_date.setText(_translate("Dialog", "作圖_日期別"))
        self.push_origin.setText(_translate("Dialog", "打開原檔"))
        self.push_average.setText(_translate("Dialog", "平均消費"))
        self.label_average.setText(_translate("Dialog", "平均消費=?"))
        self.label_4.setText(_translate("Dialog", "月"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

