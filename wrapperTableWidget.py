import os, subprocess, platform

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, pyqtSlot, QObject

class ResultTableWidgetWrapper(QObject):    
    COLUMNS_WEIGHT = [0.85, 0.15]

    def __init__(self, tableWidget:QTableWidget):
        super().__init__()   
        self.tableWidget = tableWidget
        self._setTableColumns()

        self.folderPath = ''

        self.tableWidget.itemDoubleClicked.connect(self._rowDoubleClickEvent)
        self.tableWidget.setMouseTracking(True)
        self.tableWidget.cellEntered.connect(self._onCellHover)
    
    def setFolderPath(self, folderPath:str):
        self.folderPath = folderPath

    def adjustColumnWidth(self):
        tableWidth = self.tableWidget.viewport().width()
        self.tableWidget.setColumnWidth(0, int(ResultTableWidgetWrapper.COLUMNS_WEIGHT[0] * tableWidth))
        self.tableWidget.setColumnWidth(1, int(ResultTableWidgetWrapper.COLUMNS_WEIGHT[1] * tableWidth))
    
    def clear(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

    @pyqtSlot(str, int)
    def addTableRow(self, filename:str, page:int):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(filename))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(str(page)))
    
    def _setTableColumns(self):
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        header.setSectionResizeMode(1, QHeaderView.Interactive)
    
    def _rowDoubleClickEvent(self, item):
        row = item.row()
        filenameItem = self.tableWidget.item(row, 0)
        pageItem = self.tableWidget.item(row, 1)

        if not(filenameItem and pageItem):
            return 
        
        filename = filenameItem.text()
        self._openPdfFile(filename)
    
    def _onCellHover(self, row, column):
        self.tableWidget.setCursor(Qt.PointingHandCursor)
        
    def _openPdfFile(self, filepath: str):
        fullFilePath = os.path.join(self.folderPath, filepath)
        handler = PdfOpenerFactory()
        handler.openFile(fullFilePath)

class PdfOpenerFactory:
    def __init__(self):
        self.platformHandlersDict = {
            'darwin': self._openMacOs,
            'Windows': self._openWindows,
            'linux': self._openLinux
        }
        osType = platform.system()
        self.platformOpenHandle = self.platformHandlersDict[osType]
    
    def openFile(self, filePath:str):
        self.platformOpenHandle(filePath)
    
    def _openMacOs(self, filePath:str):
        subprocess.call(('open', filePath))
    
    def _openWindows(self, filePath:str):
        os.startfile(filePath)
    
    def _openLinux(self, filePath:str):
        subprocess.call(('xdg-open', filePath))
