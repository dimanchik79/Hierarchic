from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog


class MainClass(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("UI/main.ui", self)
        self.setFixedSize(1222, 879)

        self.b_open.clicked.connect(self.open_bibliophile)

    @staticmethod
    def open_bibliophile():
        dialog = OpenBibliothec()
        dialog.show()
        dialog.exec_()
        print(dialog.result())


class OpenBibliothec(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("UI/biblio.ui", self)
        self.setFixedSize(493, 616)

