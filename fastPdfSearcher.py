import os, re, multiprocessing
import fitz

from PyQt5 import QtCore

def _searchSinglePdf(args) -> None|tuple[str, int]:
    folderPath, pdfFileName, regexPattern = args
    pdfPath = os.path.join(folderPath, pdfFileName)
    try:
        doc = fitz.open(pdfPath)
    except Exception:
        return
    
    with doc:
        for i, page in enumerate(doc):
            text = page.get_text()
            if re.search(regexPattern, text):
                return pdfFileName, i + 1

class FastPdfSearcherWorker(QtCore.QObject):
    resultFoundSignal = QtCore.pyqtSignal(str, int)   # filename, page
    finishedSignal = QtCore.pyqtSignal()

    def __init__(self, folderPath:str, pdfFiles:list[str], pattern:str):
        super().__init__()
        self.folderPath = folderPath
        self.pdfFiles = pdfFiles
        self.pattern = pattern

    def run(self):
        numOfProcesses = multiprocessing.cpu_count()        
        poolArguments = [(self.folderPath, filename, self.pattern) for filename in self.pdfFiles]

        pool = multiprocessing.Pool(processes=numOfProcesses)
        for result in pool.imap_unordered(_searchSinglePdf, poolArguments):
            if not result:
                continue
            
            filename, page = result
            self.resultFoundSignal.emit(filename, page)

        pool.close()
        pool.join()

        self.finishedSignal.emit()

    def _onFileMatched(self, result:tuple[str, int]):
        filename, page = result
        self.resultFoundSignal.emit(filename, page)

    def _splitFilesListToChunks(self, pdfFileNames:list[str], numOfChunks:int) -> list[list[str]]:
        result = [[] for _ in range(numOfChunks)]
        for i, name in enumerate(pdfFileNames):
            chunkIndex = i % numOfChunks
            result[chunkIndex].append(name)
        return result