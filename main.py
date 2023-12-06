import sys
from os import path
from PyQt5.QtWidgets import QApplication
from classes import MainClass
from models import Hierarchic, Data, Bibliophile, Current


def main():
    app = QApplication(sys.argv)
    main_window = MainClass()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    if not path.exists('DB/database.db'):
        Hierarchic.create_table()
        Data.create_table()
        Bibliophile.create_table()
        Current.create_table()
    main()
