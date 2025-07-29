import sys, os, threading

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMainWindow

from wrapperTableWidget import ResultTableWidgetWrapper
from fastPdfSearcher import FastPdfSearcher
from pdfFileFinder import PdfFileFinder

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
        self.searchFilesButton.setEnabled(False)
    
    def bindEvents(self):
        self.openFolderButton.clicked.connect(self.openFolder)
        self.searchFilesButton.clicked.connect(self.searchPDFs)

    def openFolder(self):
        def updateFilesCount(count:int):
            self.numOfFilesLabel.setText(f'Number of files: {count}')
    
        def findFilesFinished():
            self.searchFilesThread.quit()
            self.searchFilesThread.wait()
            self.resultTableWrapper.setFolderPath(self.folderPath)
            self.pdfFiles = self.worker.getPdfFiles()
            self.searchFilesButton.setEnabled(True)
        
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, False)
        dialog.setOption(QtWidgets.QFileDialog.ReadOnly, False)
        dialog.setWindowTitle('Select Directory or paste path in the "Directory" field')

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.folderPath = dialog.selectedFiles()[0]
            self.selectedFolderLabel.setText(f'Selected root folder: {self.folderPath}')

            self.worker = PdfFileFinder(self.folderPath)
            self.searchFilesThread = QtCore.QThread()
            self.worker.moveToThread(self.searchFilesThread)

            self.worker.filesCountChangedSignal.connect(updateFilesCount)
            self.worker.finishedSignal.connect(findFilesFinished)
            self.searchFilesThread.started.connect(self.worker.findPdfs)

            self.searchFilesThread.start()
    
    def searchPDFs(self):
        pattern = self.patternEdit.text()
        if not pattern:
            return 
        
        self.searchFilesButton.setEnabled(False)
        result = self.fastPdfSearcher.searchPDFs(self.folderPath, self.pdfFiles, pattern)
        self.resultTableWrapper.populateTable(result)
        self.searchFilesButton.setEnabled(True)
    
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