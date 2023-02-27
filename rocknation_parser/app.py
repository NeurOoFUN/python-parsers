import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from database import MusicDbManager
from parser import Parser


class Ui_MainWindow(QMainWindow):
    """

    The app.
    """
    def __init__(self):
        super().__init__()

        self.setObjectName("MainWindow")
        self.resize(900, 715)

        self.db_instance = MusicDbManager()
        self.parser = Parser()

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.music_list = QtWidgets.QListWidget(self)
        self.music_list.setGeometry(QtCore.QRect(0, 0, 300, 715))
        self.music_list.setObjectName("music_list")
        self.music_list.addItems(self.db_instance.show_all_groupnames())
        self.music_list.itemClicked.connect(self.parser_lounch)
        
        # self.log_list = QtWidgets.QLabel(self)
        # self.log_list.setGeometry(QtCore.QRect(310, 0, 571, 711))
        # self.log_list.setObjectName("log_list")

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

    main_window = Ui_MainWindow()

    main_window.show()

    sys.exit(app.exec_())
