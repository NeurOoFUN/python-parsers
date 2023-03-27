import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

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
        
        self.log_from_parser_module = QtWidgets.QLabel(self)
        self.log_from_parser_module.setGeometry(QtCore.QRect(310, 0, 571, 711))
        self.log_from_parser_module.setObjectName("log_from_parser_module")

        self.log_from_writer_module = QtWidgets.QLabel(self)
        self.log_from_writer_module.setGeometry(QtCore.QRect(600, 0, 571, 711))
        self.log_from_writer_module.setObjectName("log_from_writer_module")

    def parser_lounch(self, item):
        selected_group = self.db_instance.group_selection(item.text())

        if not os.path.exists(item.text()):
            os.mkdir(item.text())

        msg_box = QMessageBox()
        msg_box.setWindowTitle(' ')
        msg_box.setText('Do you need live albums?')
        msg_box.setIcon(QMessageBox.Information)
        msg_box.addButton(QMessageBox.Yes)
        msg_box.addButton(QMessageBox.No)
        msg_box.buttonClicked.connect(self.user_answer)

        msg_box.exec_()

        self.parser.link_to_selected_group = selected_group
        self.parser.group_name = item.text()
        self.parser.parse(self.log_from_parser_module, self.log_from_writer_module)

    def user_answer(self, button):
        self.parser.user_answer = button.text()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    main_window = Ui_MainWindow()

    main_window.show()

    sys.exit(app.exec_())
