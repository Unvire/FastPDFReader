from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

class ResultTableWidgetWrapper:    
    COLUMNS_WEIGHT = [0.7, 0.3]

    def __init__(self, tableWidget:QTableWidget):
        self.tableWidget = tableWidget
        self._setTableColumns()

        self.tableWidget.cellClicked.connect(self._handleRowClick)

    def adjustColumnWidth(self):
        tableWidth = self.tableWidget.viewport().width()
        self.tableWidget.setColumnWidth(0, int(ResultTableWidgetWrapper.COLUMNS_WEIGHT[0] * tableWidth))
        self.tableWidget.setColumnWidth(1, int(ResultTableWidgetWrapper.COLUMNS_WEIGHT[1] * tableWidth))
    
    def populateTable(self, searchResult:list[tuple[str, int]]):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(searchResult))
        for row, (filename, page) in enumerate(searchResult):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(filename))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(page)))
    
    def _setTableColumns(self):
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        header.setSectionResizeMode(1, QHeaderView.Interactive)
    
    def _handleRowClick(self):
        pass