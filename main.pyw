import sys, os

from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow

from wrapperTableWidget import ResultTableWidgetWrapper
from fastPdfSearcher import FastPdfSearcher

class FastPdfSearcherGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'main.ui')
        uic.loadUi(uiFilePath, self)

        self.folderPath = ""
        self.pdfFiles = []
        self.resultTableWrapper = ResultTableWidgetWrapper(self.tableWidget)
        self.fastPdfSearcher = FastPdfSearcher()
        
        self.bindEvents()
    
    def bindEvents(self):
        self.openFolderButton.clicked.connect(self.openFolder)
        self.searchFilesButton.clicked.connect(self.searchPDFs)

    def openFolder(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, False)
        dialog.setOption(QtWidgets.QFileDialog.ReadOnly, False)
        dialog.setWindowTitle('Select Directory or paste path in the "Directory" field')

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.folderPath = dialog.selectedFiles()[0]
            self.pdfFiles = [name for name in os.listdir(self.folderPath) if name.lower().endswith('.pdf')]
            self.selectedFolderLabel.setText(f'Selected folder: {self.folderPath}')
            self.numOfFilesLabel.setText(f'Number of files: {len(self.pdfFiles)}')
    
    def searchPDFs(self):
        pattern = self.patternEdit.text()
        result = self.fastPdfSearcher.searchPDFs(self.folderPath, self.pdfFiles, pattern)
        self.resultTableWrapper.populateTable(result)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.resultTableWrapper.adjustColumnWidth()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resultTableWrapper.adjustColumnWidth()
    


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FastPdfSearcherGUI()
    window.show()
    sys.exit(app.exec_())