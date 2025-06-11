from PyQt5.QtWidgets import QTableWidget, QHeaderView

class ResultTableWidgetWrapper:    
    COLUMNS_WEIGHT = [0.1, 0.7, 0.2]

    def __init__(self, tableWidget:QTableWidget):
        self.tableWidget = tableWidget
        self._setTableColumns()
    
    def _setTableColumns(self):
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        header.setSectionResizeMode(2, QHeaderView.Interactive)
        
    def adjustColumnWidth(self):
        tableWidth = self.tableWidget.viewport().width()
        self.tableWidget.setColumnWidth(0, int(ResultTableWidgetWrapper.COLUMNS_WEIGHT[0] * tableWidth))
        self.tableWidget.setColumnWidth(1, int(ResultTableWidgetWrapper.COLUMNS_WEIGHT[1] * tableWidth))
        self.tableWidget.setColumnWidth(2, int(ResultTableWidgetWrapper.COLUMNS_WEIGHT[2] * tableWidth))