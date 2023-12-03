from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class MainClass(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("UI/main.ui", self)
        self.setFixedSize(1222, 848)
