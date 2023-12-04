from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow, QDialog, QComboBox, QListWidget, QCheckBox
from models import Hierarchic, Data, Bibliophile


class MainClass(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.biblioteka = ""
        uic.loadUi("UI/main.ui", self)
        self.setFixedSize(1222, 879)

        self.b_open.clicked.connect(self.open_bibliophile)

    def open_bibliophile(self):
        dialog = OpenBibliothec()
        dialog.show()
        dialog.exec_()
        if dialog.result() == 1:
            if self.biblioteka == dialog.bibliolist.currentItem().text():
                return
            self.biblioteka = dialog.bibliolist.currentItem().text()
            self.bib_name.setText(self.biblioteka)


class OpenBibliothec(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.biblio = []
        self.sorted = 0
        uic.loadUi("UI/biblio.ui", self)
        self.setFixedSize(493, 616)
        self.add.clicked.connect(self.change_biblio)
        self.sort.clicked.connect(self.change_sort)
        self.set_position(0)

    def set_position(self, pos):
        self.update_bibliolist()
        if self.biblio and pos == 0:
            self.bibliolist.setCurrentRow(0)
            self.bibliolist.setFocus()
        elif self.biblio and pos == 1:
            self.bibliolist.setCurrentRow(self.bibliolist.count() - 1)
            self.bibliolist.setFocus()

    def change_biblio(self):
        if not self.biblio:
            return
        dialog = OpenInstrumentary(mark="biblio", current_item=self.bibliolist.currentItem().text())
        while True:
            dialog.name.setFocus()
            dialog.show()
            dialog.exec_()
            if dialog.result() == 0:
                self.bibliolist.setFocus()
                return
            if dialog.cb.currentText() == "Добавить библиотеку":
                row = [row.bibl_name for row in Bibliophile.select().where(Bibliophile.bibl_name == dialog.name.text())]
                if row:
                    dialog.name.setStyleSheet("background-color: red; color: rgb(255, 255, 255);")
                    continue
                dialog.name.setStyleSheet("background-color: rgb(63, 63, 63); color: rgb(255, 255, 255);")
                Bibliophile.create(bibl_name=dialog.name.text())
                self.set_position(1)
            elif dialog.cb.currentText() == "Переименовать библиотеку":
                # TODO
                pass

    def change_sort(self):
        if self.sorted == 0:
            self.sort.setIcon(QtGui.QIcon("IMG/az.ico"))
        if self.sorted == 1:
            self.sort.setIcon(QtGui.QIcon("IMG/za.ico"))
        if self.sorted == 2:
            self.sort.setIcon(QtGui.QIcon("IMG/sort.ico"))
            self.sorted = -1
        self.sorted += 1
        self.set_position(0)

    def update_bibliolist(self):
        self.bibliolist.clear()
        self.biblio.clear()
        self.biblio = [row.bibl_name for row in Bibliophile.select()]
        if self.sorted == 1:
            sorted_biblio = sorted(self.biblio)
        elif self.sorted == 2:
            sorted_biblio = sorted(self.biblio, reverse=True)
        else:
            sorted_biblio = self.biblio
        for biblio in sorted_biblio:
            self.bibliolist.addItem(biblio)


class OpenInstrumentary(QDialog):
    def __init__(self, mark, current_item) -> None:
        super().__init__()
        self.mark = mark
        self.current_item = current_item
        self.cb = QComboBox()
        self.closent = QCheckBox()
        uic.loadUi("UI/add_items.ui", self)
        self.setFixedSize(529, 219)

        self.cb.currentTextChanged.connect(self.change_mode)
        self.closent.clicked.connect(lambda: self.name.setFocus())
        self.r_b1.clicked.connect(lambda: self.change_char(mark=1))
        self.r_b2.clicked.connect(lambda: self.change_char(mark=2))
        self.r_b3.clicked.connect(lambda: self.change_char(mark=3))
        self.name.setFocus()

        if self.mark == "biblio":
            self.setWindowTitle("РАБОТА С БИБЛИОТЕКАМИ")
            self.cb.clear()
            self.cb.addItems(["Добавить библиотеку", "Переименовать библиотеку"])

    def change_char(self, mark):
        if mark == 1:
            self.name.setText(self.name.text().upper())
        elif mark == 2:
            self.name.setText(self.name.text().lower())
        elif mark == 3:
            self.name.setText(self.name.text().capitalize())
        self.name.setFocus()

    def change_mode(self):
        if self.cb.currentText() == "Переименовать библиотеку":
            self.name.setText(self.current_item)
        self.name.setFocus()
