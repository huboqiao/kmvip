# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\www\kmvip\src\ui\useredit.ui'
#
# Created: Wed Jun 25 22:47:26 2014
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
        Dialog.resize(542, 628)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(320, 240, 51, 30))
        self.label_6.setMinimumSize(QtCore.QSize(0, 30))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.username = QtGui.QLineEdit(Dialog)
        self.username.setGeometry(QtCore.QRect(90, 21, 210, 30))
        self.username.setMinimumSize(QtCore.QSize(0, 0))
        self.username.setMaximumSize(QtCore.QSize(16777215, 30))
        self.username.setText(_fromUtf8(""))
        self.username.setReadOnly(True)
        self.username.setObjectName(_fromUtf8("username"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 57, 61, 30))
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.password = QtGui.QLineEdit(Dialog)
        self.password.setGeometry(QtCore.QRect(90, 278, 210, 30))
        self.password.setMinimumSize(QtCore.QSize(0, 0))
        self.password.setMaximumSize(QtCore.QSize(16777215, 30))
        self.password.setText(_fromUtf8(""))
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.sex = QtGui.QComboBox(Dialog)
        self.sex.setGeometry(QtCore.QRect(90, 93, 91, 30))
        self.sex.setMaximumSize(QtCore.QSize(110, 30))
        self.sex.setObjectName(_fromUtf8("sex"))
        self.sex.addItem(_fromUtf8(""))
        self.sex.addItem(_fromUtf8(""))
        self.birthday = QtGui.QDateEdit(Dialog)
        self.birthday.setGeometry(QtCore.QRect(390, 240, 141, 30))
        self.birthday.setAccelerated(False)
        self.birthday.setCalendarPopup(True)
        self.birthday.setObjectName(_fromUtf8("birthday"))
        self.password2 = QtGui.QLineEdit(Dialog)
        self.password2.setGeometry(QtCore.QRect(390, 278, 141, 30))
        self.password2.setMinimumSize(QtCore.QSize(0, 0))
        self.password2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.password2.setText(_fromUtf8(""))
        self.password2.setEchoMode(QtGui.QLineEdit.Password)
        self.password2.setObjectName(_fromUtf8("password2"))
        self.tel = QtGui.QLineEdit(Dialog)
        self.tel.setGeometry(QtCore.QRect(90, 203, 210, 30))
        self.tel.setMinimumSize(QtCore.QSize(0, 0))
        self.tel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.tel.setText(_fromUtf8(""))
        self.tel.setObjectName(_fromUtf8("tel"))
        self.pushButton_4 = QtGui.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(420, 500, 101, 41))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 21, 61, 30))
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.hukou = QtGui.QLineEdit(Dialog)
        self.hukou.setGeometry(QtCore.QRect(90, 166, 210, 30))
        self.hukou.setMinimumSize(QtCore.QSize(0, 0))
        self.hukou.setMaximumSize(QtCore.QSize(16777215, 30))
        self.hukou.setObjectName(_fromUtf8("hukou"))
        self.pushButton_5 = QtGui.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(420, 550, 101, 41))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_8 = QtGui.QPushButton(Dialog)
        self.pushButton_8.setGeometry(QtCore.QRect(420, 390, 105, 41))
        self.pushButton_8.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.adder = QtGui.QLineEdit(Dialog)
        self.adder.setGeometry(QtCore.QRect(90, 316, 441, 30))
        self.adder.setMinimumSize(QtCore.QSize(0, 0))
        self.adder.setMaximumSize(QtCore.QSize(16777215, 30))
        self.adder.setObjectName(_fromUtf8("adder"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 240, 61, 30))
        self.label_5.setMinimumSize(QtCore.QSize(0, 30))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.group = QtGui.QComboBox(Dialog)
        self.group.setGeometry(QtCore.QRect(90, 130, 91, 30))
        self.group.setMaximumSize(QtCore.QSize(110, 30))
        self.group.setObjectName(_fromUtf8("group"))
        self.label_15 = QtGui.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(320, 280, 61, 30))
        self.label_15.setMinimumSize(QtCore.QSize(0, 30))
        self.label_15.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(20, 203, 61, 30))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.card = QtGui.QLineEdit(Dialog)
        self.card.setGeometry(QtCore.QRect(90, 240, 210, 30))
        self.card.setMinimumSize(QtCore.QSize(0, 0))
        self.card.setMaximumSize(QtCore.QSize(16777215, 30))
        self.card.setText(_fromUtf8(""))
        self.card.setObjectName(_fromUtf8("card"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(20, 166, 61, 30))
        self.label_7.setMinimumSize(QtCore.QSize(0, 30))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(20, 93, 61, 30))
        self.label_11.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_14 = QtGui.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(20, 130, 61, 30))
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.nickname = QtGui.QLineEdit(Dialog)
        self.nickname.setGeometry(QtCore.QRect(90, 57, 210, 30))
        self.nickname.setMinimumSize(QtCore.QSize(0, 0))
        self.nickname.setMaximumSize(QtCore.QSize(16777215, 30))
        self.nickname.setText(_fromUtf8(""))
        self.nickname.setObjectName(_fromUtf8("nickname"))
        self.label_16 = QtGui.QLabel(Dialog)
        self.label_16.setGeometry(QtCore.QRect(20, 278, 61, 30))
        self.label_16.setMinimumSize(QtCore.QSize(0, 30))
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(320, 20, 211, 211))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.frame = QtGui.QWidget(self.groupBox)
        self.frame.setGeometry(QtCore.QRect(10, 20, 191, 181))
        self.frame.setObjectName(_fromUtf8("frame"))
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(20, 360, 104, 30))
        self.label_8.setMinimumSize(QtCore.QSize(0, 30))
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_8.setText(_fromUtf8(""))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(20, 316, 61, 30))
        self.label_9.setMinimumSize(QtCore.QSize(0, 30))
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(420, 350, 31, 30))
        self.label_10.setMinimumSize(QtCore.QSize(0, 30))
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_10.setText(_fromUtf8(""))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 360, 351, 261))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.shenfenzheng = QtGui.QPushButton(self.tab)
        self.shenfenzheng.setGeometry(QtCore.QRect(130, 200, 102, 30))
        self.shenfenzheng.setMinimumSize(QtCore.QSize(0, 30))
        self.shenfenzheng.setObjectName(_fromUtf8("shenfenzheng"))
        self.shenfenzhengimage = QtGui.QWidget(self.tab)
        self.shenfenzhengimage.setGeometry(QtCore.QRect(10, 10, 331, 181))
        self.shenfenzhengimage.setObjectName(_fromUtf8("shenfenzhengimage"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.shenfenzheng_t = QtGui.QPushButton(self.tab_2)
        self.shenfenzheng_t.setGeometry(QtCore.QRect(120, 200, 102, 30))
        self.shenfenzheng_t.setMinimumSize(QtCore.QSize(0, 30))
        self.shenfenzheng_t.setObjectName(_fromUtf8("shenfenzheng_t"))
        self.shenfenzhengimage_t = QtGui.QWidget(self.tab_2)
        self.shenfenzhengimage_t.setGeometry(QtCore.QRect(10, 10, 331, 181))
        self.shenfenzhengimage_t.setObjectName(_fromUtf8("shenfenzhengimage_t"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.pushButton_6 = QtGui.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(420, 450, 105, 41))
        self.pushButton_6.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "修改员工信息", None))
        self.label_6.setText(_translate("Dialog", "生    日：", None))
        self.label_2.setText(_translate("Dialog", "姓    名：", None))
        self.sex.setItemText(0, _translate("Dialog", "女", None))
        self.sex.setItemText(1, _translate("Dialog", "男", None))
        self.pushButton_4.setText(_translate("Dialog", "修改", None))
        self.label.setText(_translate("Dialog", "登 录 名：", None))
        self.pushButton_5.setText(_translate("Dialog", "取消", None))
        self.pushButton_8.setText(_translate("Dialog", "指纹录入", None))
        self.label_5.setText(_translate("Dialog", "身 份 证：", None))
        self.label_15.setText(_translate("Dialog", "确认密码：", None))
        self.label_13.setText(_translate("Dialog", "联系电话：", None))
        self.label_7.setText(_translate("Dialog", "户    籍：", None))
        self.label_11.setText(_translate("Dialog", "性    别：", None))
        self.label_14.setText(_translate("Dialog", "所 在 组：", None))
        self.label_16.setText(_translate("Dialog", "密   码：", None))
        self.groupBox.setTitle(_translate("Dialog", "照片", None))
        self.label_9.setText(_translate("Dialog", "住宅地址：", None))
        self.shenfenzheng.setText(_translate("Dialog", "选择图像", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "身份证正面", None))
        self.shenfenzheng_t.setText(_translate("Dialog", "选择图像", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "身份证反面", None))
        self.pushButton_6.setText(_translate("Dialog", "拍照", None))
