# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'losingcard.ui'
#
# Created: Tue Mar 03 16:59:20 2015
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(856, 542)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 30, 54, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(110, 30, 141, 21))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(310, 10, 101, 41))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(30, 60, 501, 291))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 54, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.membername = QtGui.QLineEdit(self.groupBox)
        self.membername.setGeometry(QtCore.QRect(80, 30, 141, 21))
        self.membername.setObjectName(_fromUtf8("membername"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 54, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.cardid = QtGui.QLineEdit(self.groupBox)
        self.cardid.setGeometry(QtCore.QRect(80, 70, 141, 21))
        self.cardid.setObjectName(_fromUtf8("cardid"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 112, 54, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.sex = QtGui.QComboBox(self.groupBox)
        self.sex.setGeometry(QtCore.QRect(80, 110, 69, 21))
        self.sex.setObjectName(_fromUtf8("sex"))
        self.sex.addItem(_fromUtf8(""))
        self.sex.addItem(_fromUtf8(""))
        self.sex.addItem(_fromUtf8(""))
        self.sex.setItemText(2, _fromUtf8(""))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 150, 54, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.tel = QtGui.QLineEdit(self.groupBox)
        self.tel.setGeometry(QtCore.QRect(80, 150, 141, 21))
        self.tel.setObjectName(_fromUtf8("tel"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(20, 190, 54, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.nation = QtGui.QLineEdit(self.groupBox)
        self.nation.setGeometry(QtCore.QRect(80, 190, 141, 21))
        self.nation.setObjectName(_fromUtf8("nation"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(20, 230, 54, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.idcard = QtGui.QLineEdit(self.groupBox)
        self.idcard.setGeometry(QtCore.QRect(80, 230, 141, 21))
        self.idcard.setObjectName(_fromUtf8("idcard"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(250, 20, 231, 191))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.widget_2 = QtGui.QWidget(self.groupBox_2)
        self.widget_2.setGeometry(QtCore.QRect(30, 30, 181, 141))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(20, 260, 54, 21))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.adder = QtGui.QLineEdit(self.groupBox)
        self.adder.setGeometry(QtCore.QRect(80, 260, 211, 20))
        self.adder.setObjectName(_fromUtf8("adder"))
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(250, 222, 54, 21))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.carddate = QtGui.QLineEdit(self.groupBox)
        self.carddate.setGeometry(QtCore.QRect(310, 220, 131, 21))
        self.carddate.setObjectName(_fromUtf8("carddate"))
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 360, 501, 161))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.widget = QtGui.QWidget(self.groupBox_3)
        self.widget.setGeometry(QtCore.QRect(110, 20, 241, 121))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(540, 20, 261, 151))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.label_10 = QtGui.QLabel(self.groupBox_4)
        self.label_10.setGeometry(QtCore.QRect(10, 30, 54, 21))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.relativesname = QtGui.QLineEdit(self.groupBox_4)
        self.relativesname.setGeometry(QtCore.QRect(80, 30, 121, 21))
        self.relativesname.setObjectName(_fromUtf8("relativesname"))
        self.label_11 = QtGui.QLabel(self.groupBox_4)
        self.label_11.setGeometry(QtCore.QRect(10, 60, 54, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.relativessex = QtGui.QComboBox(self.groupBox_4)
        self.relativessex.setGeometry(QtCore.QRect(80, 60, 69, 21))
        self.relativessex.setObjectName(_fromUtf8("relativessex"))
        self.relativessex.addItem(_fromUtf8(""))
        self.relativessex.addItem(_fromUtf8(""))
        self.relativessex.addItem(_fromUtf8(""))
        self.relativessex.setItemText(2, _fromUtf8(""))
        self.label_12 = QtGui.QLabel(self.groupBox_4)
        self.label_12.setGeometry(QtCore.QRect(10, 90, 54, 21))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.relationship = QtGui.QLineEdit(self.groupBox_4)
        self.relationship.setGeometry(QtCore.QRect(80, 90, 121, 21))
        self.relationship.setObjectName(_fromUtf8("relationship"))
        self.label_13 = QtGui.QLabel(self.groupBox_4)
        self.label_13.setGeometry(QtCore.QRect(10, 120, 54, 21))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.relationtem = QtGui.QLineEdit(self.groupBox_4)
        self.relationtem.setGeometry(QtCore.QRect(80, 120, 121, 21))
        self.relationtem.setObjectName(_fromUtf8("relationtem"))
        self.groupBox_5 = QtGui.QGroupBox(Dialog)
        self.groupBox_5.setGeometry(QtCore.QRect(540, 180, 271, 191))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.records_txt = QtGui.QTextEdit(self.groupBox_5)
        self.records_txt.setGeometry(QtCore.QRect(20, 20, 231, 41))
        self.records_txt.setObjectName(_fromUtf8("records_txt"))
        self.records_txt_2 = QtGui.QTextEdit(self.groupBox_5)
        self.records_txt_2.setGeometry(QtCore.QRect(20, 60, 231, 41))
        self.records_txt_2.setObjectName(_fromUtf8("records_txt_2"))
        self.records_txt_3 = QtGui.QTextEdit(self.groupBox_5)
        self.records_txt_3.setGeometry(QtCore.QRect(20, 100, 231, 41))
        self.records_txt_3.setObjectName(_fromUtf8("records_txt_3"))
        self.records_txt_4 = QtGui.QTextEdit(self.groupBox_5)
        self.records_txt_4.setGeometry(QtCore.QRect(20, 140, 231, 41))
        self.records_txt_4.setObjectName(_fromUtf8("records_txt_4"))
        self.groupBox_6 = QtGui.QGroupBox(Dialog)
        self.groupBox_6.setGeometry(QtCore.QRect(540, 370, 271, 151))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.label_14 = QtGui.QLabel(self.groupBox_6)
        self.label_14.setGeometry(QtCore.QRect(20, 30, 54, 21))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.lineEdit_12 = QtGui.QLineEdit(self.groupBox_6)
        self.lineEdit_12.setGeometry(QtCore.QRect(80, 30, 161, 21))
        self.lineEdit_12.setObjectName(_fromUtf8("lineEdit_12"))
        self.label_15 = QtGui.QLabel(self.groupBox_6)
        self.label_15.setGeometry(QtCore.QRect(20, 60, 54, 21))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.lineEdit_13 = QtGui.QLineEdit(self.groupBox_6)
        self.lineEdit_13.setGeometry(QtCore.QRect(80, 60, 161, 21))
        self.lineEdit_13.setObjectName(_fromUtf8("lineEdit_13"))
        self.label_16 = QtGui.QLabel(self.groupBox_6)
        self.label_16.setGeometry(QtCore.QRect(20, 90, 54, 21))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.lineEdit_14 = QtGui.QLineEdit(self.groupBox_6)
        self.lineEdit_14.setGeometry(QtCore.QRect(80, 90, 161, 21))
        self.lineEdit_14.setObjectName(_fromUtf8("lineEdit_14"))
        self.label_17 = QtGui.QLabel(self.groupBox_6)
        self.label_17.setGeometry(QtCore.QRect(20, 120, 54, 21))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.lineEdit_15 = QtGui.QLineEdit(self.groupBox_6)
        self.lineEdit_15.setGeometry(QtCore.QRect(80, 120, 161, 21))
        self.lineEdit_15.setObjectName(_fromUtf8("lineEdit_15"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(430, 10, 101, 41))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "绑定卡", None))
        self.label.setText(_translate("Dialog", "身份证号：", None))
        self.pushButton.setText(_translate("Dialog", "挂失卡", None))
        self.groupBox.setTitle(_translate("Dialog", "客户基本资料", None))
        self.label_2.setText(_translate("Dialog", "客户姓名：", None))
        self.label_3.setText(_translate("Dialog", "会员卡号：", None))
        self.label_4.setText(_translate("Dialog", "性   别：", None))
        self.sex.setItemText(0, _translate("Dialog", "女", None))
        self.sex.setItemText(1, _translate("Dialog", "男", None))
        self.label_5.setText(_translate("Dialog", "联系电话：", None))
        self.label_6.setText(_translate("Dialog", "民   族：", None))
        self.label_7.setText(_translate("Dialog", "身份证号：", None))
        self.groupBox_2.setTitle(_translate("Dialog", "照片", None))
        self.label_8.setText(_translate("Dialog", "联系地址：", None))
        self.label_9.setText(_translate("Dialog", "有效期：", None))
        self.groupBox_3.setTitle(_translate("Dialog", "身份证扫描证", None))
        self.groupBox_4.setTitle(_translate("Dialog", "亲属信息", None))
        self.label_10.setText(_translate("Dialog", "姓名：", None))
        self.label_11.setText(_translate("Dialog", "性别：", None))
        self.relativessex.setItemText(0, _translate("Dialog", "女", None))
        self.relativessex.setItemText(1, _translate("Dialog", "男", None))
        self.label_12.setText(_translate("Dialog", "关系：", None))
        self.label_13.setText(_translate("Dialog", "手机：", None))
        self.groupBox_5.setTitle(_translate("Dialog", "近期交易明细", None))
        self.groupBox_6.setTitle(_translate("Dialog", "银行信息", None))
        self.label_14.setText(_translate("Dialog", "开户名：", None))
        self.label_15.setText(_translate("Dialog", "开户行：", None))
        self.label_16.setText(_translate("Dialog", "开户帐号：", None))
        self.label_17.setText(_translate("Dialog", "开户点：", None))
        self.pushButton_2.setText(_translate("Dialog", "用户忘记密码", None))
