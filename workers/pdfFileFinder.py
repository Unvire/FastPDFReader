from PyQt5 import QtCore
import os

class PdfFileFinder(QtCore.QObject):
    filesCountChangedSignal = QtCore.pyqtSignal(int)
    finishedSignal = QtCore.pyqtSignal()

    def __init__(self, folderPath:str):
        super().__init__()
        self.folderPath = folderPath
        self.pdfFiles = []
        
        self._isRunning = False

    def findPdfs(self):
        numOfFiles = 0
        self._isRunning = True
        for subFolder, _, files in os.walk(self.folderPath):
            if not self._isRunning:
                break
            
            for fileName in files:
                if not self._isRunning:
                    break

                if not fileName.lower().endswith('.pdf'):
                    continue

                full_path = os.path.join(subFolder, fileName)
                self.pdfFiles.append(full_path)
                numOfFiles += 1
                self.filesCountChangedSignal.emit(numOfFiles)
        
        self.finishedSignal.emit()
        self.stop()
    
    def getPdfFiles(self) -> list[str]:
        return self.pdfFiles

    def stop(self):
        self._isRunning = False