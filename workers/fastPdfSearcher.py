import os, re, multiprocessing
import fitz

from PyQt5 import QtCore

def _searchSinglePdf(args) -> None|tuple[str, int]:
    folderPath, pdfFileName, regexPattern, isFileNamesOnly, stopFlag = args
    pdfPath = os.path.join(folderPath, pdfFileName)
    try:
        doc = fitz.open(pdfPath)
    except Exception:
        return
    
    with doc:
        if stopFlag.value:
            return

        baseFileName = os.path.basename(pdfFileName).split('.')[0]
        if re.search(regexPattern, baseFileName):
            return pdfFileName, 0
        
        if not isFileNamesOnly:
            try:
                for i, page in enumerate(doc):
                    text = page.get_text()
                    if re.search(regexPattern, text):
                        return pdfFileName, i + 1
            except Exception:
                return

class FastPdfSearcherWorker(QtCore.QObject):
    resultFoundSignal = QtCore.pyqtSignal(str, int)   # filename, page
    finishedSignal = QtCore.pyqtSignal()
    progressSignal = QtCore.pyqtSignal(int)

    def __init__(self, folderPath:str, pdfFiles:list[str], pattern:str, isFileNamesOnly:bool):
        super().__init__()
        self.folderPath = folderPath
        self.pdfFiles = pdfFiles
        self.numOfFiles = len(pdfFiles)
        self.pattern = pattern
        self.isFileNamesOnly = isFileNamesOnly

        self.pool = None
        self.isForcedTerminate = False
        self.manager = None

    def run(self):        
        self.manager = multiprocessing.Manager()
        stopFlag = self.manager.Value('b', False)

        numOfProcesses = multiprocessing.cpu_count()       
        poolArguments = [(self.folderPath, filename, self.pattern, self.isFileNamesOnly, stopFlag) for filename in self.pdfFiles]

        self.pool = multiprocessing.Pool(processes=numOfProcesses)
        i = 0
        for result in self.pool.imap_unordered(_searchSinglePdf, poolArguments):
            if self.isForcedTerminate:
                stopFlag.value = True
                break

            if result:            
                filename, page = result
                self.resultFoundSignal.emit(filename, page)

            progress = int(100 * (i + 1) / self.numOfFiles)
            self.progressSignal.emit(progress)
            i += 1

        self.pool.close()
        self.pool.join()

        self.finishedSignal.emit()
    
    def stop(self):
        self.isForcedTerminate = True
        if self.pool:
            self.pool.terminate()