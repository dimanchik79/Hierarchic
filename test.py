import sys
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *


class ListWidget(QListWidget):
    def clicked(self, item):
        QMessageBox.information(self, "ListWidget", "Вы выбрали: "+item.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    listWidget = ListWidget()
    listWidget.resize(550, 200)

    listWidget.addItem("Item 1")
    listWidget.addItem("Item 2")
    listWidget.addItem("Item 3")

    item = QListWidgetItem()
    icon = QIcon('/IMG/folder.png')
    item.setIcon(icon)
    item.setText(" QListWidget \n https://doc.qt.io/qt-5/search-results.html?q=QListWidget")
    listWidget.addItem(item)
    listWidget.setIconSize(QSize(46, 46))
    listWidget.setFont( QFont( "Times", 12, QFont.Black ) )

    listWidget.setWindowTitle('Пример QListwidget')

    listWidget.itemClicked.connect(listWidget.clicked)

    listWidget.show()
    sys.exit(app.exec_())
