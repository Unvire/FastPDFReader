import sys, os

from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QHeaderView

class FastPdfSearcherGUI(QMainWindow):
    COLUMNS_WEIGHT = [0.1, 0.7, 0.2]
    def __init__(self):
        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'main.ui')
        uic.loadUi(uiFilePath, self)

        self._setTableColumns()
    
    def _setTableColumns(self,):
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        header.setSectionResizeMode(2, QHeaderView.Interactive)

    def showEvent(self, event):
        super().showEvent(event)
        self.adjustColumnWidth()

    def resizeEvent(self, event):
        self.adjustColumnWidth()
        super().resizeEvent(event)

    def adjustColumnWidth(self):
        tableWidth = self.tableWidget.viewport().width()
        self.tableWidget.setColumnWidth(0, int(FastPdfSearcherGUI.COLUMNS_WEIGHT[0] * tableWidth))
        self.tableWidget.setColumnWidth(1, int(FastPdfSearcherGUI.COLUMNS_WEIGHT[1] * tableWidth))
        self.tableWidget.setColumnWidth(2, int(FastPdfSearcherGUI.COLUMNS_WEIGHT[2] * tableWidth))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FastPdfSearcherGUI()
    window.show()
    sys.exit(app.exec_())