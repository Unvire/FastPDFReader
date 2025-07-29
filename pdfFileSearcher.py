from PyQt5 import QtCore
import os

class PdfFileSearcher(QtCore.QObject):
    filesCountChangedSignal = QtCore.pyqtSignal(int)
    finishedSignal = QtCore.pyqtSignal()

    def __init__(self, folderPath:str):
        super().__init__()
        self.folderPath = folderPath
        self.pdfFiles = []

    def searchPdfs(self):
        numOfFiles = 0
        for subFolder, _, files in os.walk(self.folderPath):
            for fileName in files:
                if not fileName.lower().endswith('.pdf'):
                    continue

                full_path = os.path.join(subFolder, fileName)
                self.pdfFiles.append(full_path)
                numOfFiles += 1
                self.filesCountChangedSignal.emit(numOfFiles)
        
        self.finishedSignal.emit()