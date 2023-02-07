import os

from PyQt5 import QtCore, QtGui, QtWidgets

from database import MusicDbManager
from parser import parse


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(895, 714)

        self.db_instance = MusicDbManager()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.music_list = QtWidgets.QListWidget(self.centralwidget)
        self.music_list.setGeometry(QtCore.QRect(0, 0, 280, 711))
        self.music_list.setObjectName("music_list")
        self.music_list.addItems(self.db_instance.show_all_groupnames())
        self.music_list.itemClicked.connect(self.get_group_name_from_db)

        self.log_list = QtWidgets.QListView(self.centralwidget)
        self.log_list.setGeometry(QtCore.QRect(310, 0, 571, 711))
        self.log_list.setObjectName("log_list")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def get_group_name_from_db(self, item):
        selected_group = self.db_instance.group_selection(item.text())

        if not os.path.exists(item.text()):
            os.mkdir(item.text())

        parse(LINK_TO_SELECTED_GROUP=selected_group, ANSWER='no', GROUP_NAME=item.text())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()


    sys.exit(app.exec_())
