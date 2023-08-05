from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

TITLE = "ftrack ams tool"
WINDOW_W = 500
WINDOW_H = 300


def user_interface(username):
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()

    window.setWindowTitle(TITLE)
    window.setGeometry(0, 0, WINDOW_W, WINDOW_H)

    # layout = QtWidgets.QVBoxLayout()
    # widget = QWidget()
    # widget.setLayout(layout)
    # window.setCentralWidget(widget)

    # label = QLabel(f"Hello, {username}! 👋")
    # layout.addWidget(label)
    # question = QLabel("What do you want to do today???? 🥳")
    # layout.addWidget(question)

    # btn_new_proj = QtWidgets.QPushButton("Create new project")
    # layout.addWidget(btn_new_proj)
    # btn_new_proj.connect()
    # new_proj = NewProjectWidget()

    # btn_add_proj = QtWidgets.QPushButton("Add to existing project")
    # layout.addWidget(btn_add_proj)

    user = UserMenu(window, username)
    new_proj = NewProjectWidget(window)
    new_proj.hide()

    user.show()
    window.show()

    user.btn_new.clicked.connect(user.hide)

    user.btn_new.clicked.connect(new_proj.show)
    app.exec_()


class UserMenu(QWidget):
    def __init__(self, parent, username):
        super(UserMenu, self).__init__(parent)
        greeting = QLabel(f"hey {username} 👋")
        question = QLabel("What are we doing today? 🤩")
        self.btn_new = QtWidgets.QPushButton("Create new project..")
        self.btn_add = QtWidgets.QPushButton("Add to existing project..")
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(greeting, 0, 0)
        self.layout.addWidget(question, 1, 0)
        self.layout.addWidget(self.btn_new, 2, 0)
        self.layout.addWidget(self.btn_add, 2, 1)
        self.setGeometry(0, 0, WINDOW_W, WINDOW_H)


class NewProjectWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(NewProjectWidget, self).__init__(parent)
        self.layout = QtWidgets.QGridLayout(self)
        label = QLabel("Making a new project 🤩")

        projnumberlabel = QLabel("Project number:")
        self.projnumber = QLineEdit(self)

        clientcodelabel = QLabel("Client code:")
        self.clientcode = QLineEdit(self)

        projcodelabel = QLabel("Project code:")
        self.projcode = QLineEdit(self)

        self.btn_back = QPushButton("Back")
        self.btn_next = QPushButton("Next")

        self.layout.addWidget(label, 0, 0)

        self.layout.addWidget(projnumberlabel, 1, 0)
        self.layout.addWidget(self.projnumber, 1, 1)

        self.layout.addWidget(clientcodelabel, 2, 0)
        self.layout.addWidget(self.clientcode, 2, 1)

        self.layout.addWidget(projcodelabel, 3, 0)
        self.layout.addWidget(self.projcode, 3, 1)

        self.layout.addWidget(self.btn_back, 4, 0)
        self.layout.addWidget(self.btn_next, 4, 1)
        self.setGeometry(0, 0, WINDOW_W, WINDOW_H)


if __name__ == "__main__":
    user_interface("Lucas.Selfslagh")
