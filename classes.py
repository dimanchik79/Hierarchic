from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QComboBox, QListWidget, QCheckBox
from models import Hierarchic, Data, Bibliophile


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
        self.biblio = []
        uic.loadUi("UI/biblio.ui", self)
        self.setFixedSize(493, 616)
        self.add.clicked.connect(self.add_biblio)

        self.update_bibiliolist()

        if self.biblio:
            self.bibliolist.setCurrentRow(0)
            self.bibliolist.setFocus()

    def add_biblio(self):
        dialog = OpenInstrumentary(mark="biblio", current_biblio=self.bibliolist.currentItem().text())
        while dialog.closent.checkState() == 2:
            dialog.name.setFocus()
            dialog.show()
            dialog.exec_()
            if dialog.result() == 0:
                break
            if dialog.cb.currentText() == "Добавить библиотеку":
                # TODO
                pass
            else:
                # TODO
                pass

    def update_bibiliolist(self):
        self.bibliolist.clear()
        self.biblio.clear()
        self.biblio = [row.bibl_name for row in Bibliophile.select()]
        self.biblio.sort()
        for biblio in self.biblio:
            self.bibliolist.addItem(biblio)


class OpenInstrumentary(QDialog):
    def __init__(self, mark, current_biblio) -> None:
        super().__init__()
        self.mark = mark
        self.current_biblio = current_biblio
        self.cb = QComboBox()
        self.closent = QCheckBox()
        uic.loadUi("UI/add_items.ui", self)
        self.setFixedSize(529, 219)

        self.cb.currentTextChanged.connect(lambda: self.name.setFocus())
        self.closent.clicked.connect(lambda: self.name.setFocus())
        self.r_b1.clicked.connect(lambda: self.name.setFocus())
        self.r_b2.clicked.connect(lambda: self.name.setFocus())
        self.r_b3.clicked.connect(lambda: self.name.setFocus())
        self.r_b4.clicked.connect(lambda: self.name.setFocus())
        self.name.setFocus()

        if self.mark == "biblio":
            self.setWindowTitle("РАБОТА С БИБЛИОТЕКАМИ")
            self.cb.clear()
            self.cb.addItems(["Добавить библиотеку", "Переименовать библиотеку"])
