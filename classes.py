from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QDialog, QComboBox

from models import Hierarchic, Bibliophile, Current


class MainClass(QMainWindow):
    def __init__(self, parent=None) -> None:
        super(MainClass, self).__init__(parent)
        self.catalogs = QtWidgets.QListWidget()
        self.biblioteka = ""
        self.path = ""
        self.parent_item = []
        self.id_path = ""
        self.level = 0

        uic.loadUi("UI/main.ui", self)
        self.setFixedSize(1222, 879)
        self.b_open.clicked.connect(self.open_bibliophile)
        self.b_add.clicked.connect(self.change_catalog)
        self.first_open_bibliothec()

    def save_current_bibl(self):
        """Метод сохраняет выбранную библиотеку для последующего открытия"""
        Current.delete().execute()
        Current.create(bibl_name=self.biblioteka, parent="", level=0, path="")

    def first_open_bibliothec(self):
        current = [row for row in Current.select().where(Current.id == 1)]
        if not current:
            return
        self.biblioteka = current[0].bibl_name
        self.parent_item.append("" if current[0].parent == "" else current[0].parent)
        self.level = current[0].level
        self.path = current[0].path
        self.bib_name.setText(f"{self.biblioteka}")
        self.open_level_documents()

    def open_bibliophile(self):
        dialog = OpenBibliothec()
        dialog.show()
        dialog.exec_()
        if dialog.result() == 1:
            if self.biblioteka == dialog.bibliolist.currentItem().text():
                return
            self.biblioteka = dialog.bibliolist.currentItem().text()
            self.save_current_bibl()
            self.bib_name.setText(f"{self.biblioteka}")
            self.open_level_documents()

    def open_level_documents(self):
        rows = [row for row in Hierarchic.select().where(Hierarchic.bibl_name == self.biblioteka,
                                                         Hierarchic.level == self.level,
                                                         Hierarchic.parent == self.parent_item[self.level])]
        if not rows:
            return
        self.catalogs.clear()
        for row in rows:
            if row.mark == 0:
                item = QtWidgets.QListWidgetItem(QtGui.QIcon('IMG/folder.ico'), row.name_docum)
                self.catalogs.setIconSize(QSize(18, 18))
                self.catalogs.addItem(item)
        self.catalogs.setCurrentRow(len(rows) - 1)
        self.catalogs.setFocus()

    def change_catalog(self):
        if self.bib_name.text() == "":
            dialog = OpenError(error_msg="Откройте имеющуюся библиотеку\nили создайте новую")
            dialog.show()
            dialog.exec_()
            return
        dialog = OpenInstrumentary(mark="tree", current_item="")
        dialog.cb.clear()
        dialog.cb.addItems(["Добавить каталог", "Добавить документ"])
        if self.catalogs.currentItem() is not None:
            dialog.cb.addItem("Переименовать текущий элемент")

        while True:
            dialog.name.setFocus()
            dialog.show()
            dialog.exec_()
            if dialog.result() == 0:
                self.catalogs.setFocus()
                return

            if dialog.cb.currentText() == "Добавить каталог":
                # TODO добавить каталог
                Hierarchic.create(bibl_name=self.biblioteka,
                                  mark=0,
                                  name_docum=dialog.name.text(),
                                  parent="" if self.level == 0 else self.parent_item[self.level - 1],
                                  level=self.level,
                                  path="" if self.level == 0 else "добавть опеределение пути")
                self.open_level_documents()
                break

            if dialog.cb.currentText() == "Добавить документ":
                # TODO добавить документ
                break

            if dialog.cb.currentText() == "Переименовать текущий элемент":
                # TODO добавить документ
                break


class OpenBibliothec(QDialog):
    def __init__(self) -> None:
        super().__init__()
        (self.biblio, self.sorted, self.last_position) = [[], 0, 0]
        uic.loadUi("UI/biblio.ui", self)
        self.setFixedSize(493, 616)
        self.add.clicked.connect(self.change_biblio)
        self.sort.clicked.connect(self.change_sort)
        self.set_position(0)

    def set_position(self, pos):
        self.update_bibliolist()
        if self.biblio and pos == 0:
            self.bibliolist.setCurrentRow(0)
        elif self.biblio and pos == 1:
            self.bibliolist.setCurrentRow(self.bibliolist.count() - 1)
        elif self.biblio and pos == 2:
            self.bibliolist.setCurrentRow(self.last_position)
        self.bibliolist.setFocus()

    def change_biblio(self):
        dialog = OpenInstrumentary(mark="biblio",
                                   current_item="" if not self.biblio else self.bibliolist.currentItem().text())
        dialog.cb.clear()
        dialog.cb.addItems(["Добавить библиотеку"])
        if self.biblio:
            dialog.cb.addItem("Переименовать библиотеку")

        while True:
            dialog.name.setFocus()
            dialog.show()
            dialog.exec_()
            if dialog.result() == 0:
                self.bibliolist.setFocus()
                return
            rows = [row.bibl_name for row in Bibliophile.select().where(Bibliophile.bibl_name == dialog.name.text())]
            if rows or dialog.name.text() == "":
                dialog.name.setStyleSheet("background-color: red; color: rgb(255, 255, 255);")
                continue
            dialog.name.setStyleSheet("background-color: rgb(63, 63, 63); color: rgb(255, 255, 255);")
            if dialog.cb.currentText() == "Добавить библиотеку":
                Bibliophile.create(bibl_name=dialog.name.text())
                self.set_position(1)
                break
            elif dialog.cb.currentText() == "Переименовать библиотеку":
                self.last_position = self.bibliolist.currentRow()
                old_name = [name for name in Bibliophile.select().where(Bibliophile.bibl_name ==
                                                                        self.bibliolist.currentItem().text())]
                old_name[0].bibl_name = dialog.name.text()
                old_name[0].save()
                self.set_position(2)
                break

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
        uic.loadUi("UI/add_items.ui", self)
        self.setFixedSize(529, 219)

        self.cb.currentTextChanged.connect(self.change_mode)
        self.name.textChanged.connect(self.modified_text)
        self.r_b1.clicked.connect(lambda: self.change_char(mark=1))
        self.r_b2.clicked.connect(lambda: self.change_char(mark=2))
        self.r_b3.clicked.connect(lambda: self.change_char(mark=3))
        self.r_b4.clicked.connect(lambda: self.change_char(mark=0))
        self.name.setFocus()

        if self.mark == "biblio":
            self.setWindowTitle("РАБОТА С БИБЛИОТЕКАМИ")

    def change_char(self, mark):
        if mark == 1:
            self.name.setText(self.name.text().upper())
        elif mark == 2:
            self.name.setText(self.name.text().lower())
        elif mark == 3:
            self.name.setText(self.name.text().capitalize())
        self.name.setFocus()

    def modified_text(self):
        if self.r_b1.isChecked():
            self.change_char(mark=1)
        elif self.r_b2.isChecked():
            self.change_char(mark=2)
        elif self.r_b3.isChecked():
            self.change_char(mark=3)

    def change_mode(self):
        if self.cb.currentText() == "Переименовать библиотеку":
            self.name.setText(self.current_item)
        self.name.setFocus()


class OpenError(QDialog):
    def __init__(self, error_msg) -> None:
        super().__init__()
        uic.loadUi("UI/error.ui", self)
        self.setFixedSize(400, 150)
        self.msg.setText(error_msg)
