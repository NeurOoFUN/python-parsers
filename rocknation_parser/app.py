import os

from PyQt5 import QtCore, QtGui, QtWidgets

from database import MusicDbManager
from parser import Parser


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(895, 714)

        self.db_instance = MusicDbManager()
        self.parser = Parser()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.music_list = QtWidgets.QListWidget(self.centralwidget)
        self.music_list.setGeometry(QtCore.QRect(0, 0, 300, 711))
        self.music_list.setObjectName("music_list")
        self.music_list.addItems(self.db_instance.show_all_groupnames())
        self.music_list.itemClicked.connect(self.parser_lounch)

        # self.log_list = QtWidgets.QListWidget(self.centralwidget)
        # self.log_list.setGeometry(QtCore.QRect(310, 0, 571, 711))
        # self.log_list.setObjectName("log_list")
        # self.log_list.addItems(data_list)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def parser_lounch(self, item):
        selected_group = self.db_instance.group_selection(item.text())

        if not os.path.exists(item.text()):
            os.mkdir(item.text())

        self.parser.link_to_selected_group = selected_group
        # self.parser.answer = selected_group
        self.parser.group_name = item.text()
        self.parser.parse()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())
