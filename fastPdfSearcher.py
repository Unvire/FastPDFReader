import os, re, multiprocessing
import fitz

from PyQt5 import QtCore

def _searchPdfChunk(args):
    return FastPdfSearcher.searchPdfChunk(args)

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
        chunks = self._splitFilesListToChunks(self.pdfFiles, numOfProcesses)

        with multiprocessing.Pool(processes=numOfProcesses) as pool:
            for chunk in chunks:
                pool.apply_async(
                    _searchPdfChunk,
                    args=((self.folderPath, chunk, self.pattern),),
                    callback=self._onChunkReady
                )
            pool.close()
            pool.join()

        self.finishedSignal.emit()

    def _onChunkReady(self, chunk_result: list[tuple[str, int]]):
        for filename, page in chunk_result:
            self.resultFoundSignal.emit(filename, page)

    def _splitFilesListToChunks(self, pdfFileNames:list[str], numOfChunks:int) -> list[list[str]]:
        result = [[] for _ in range(numOfChunks)]
        for i, name in enumerate(pdfFileNames):
            chunkIndex = i % numOfChunks
            result[chunkIndex].append(name)
        return result

class FastPdfSearcher:
    @staticmethod
    def searchPdfChunk(processArguments) -> list[tuple[str, int]]:
        folderPath, pdfFileNames, regexPattern = processArguments
        result = []
        for pdfFileName in pdfFileNames:
            pdfFilePath = os.path.join(folderPath, pdfFileName)
            try:
                file = fitz.open(pdfFilePath)
            except Exception as e:
                print(f'Error in opening {pdfFilePath}: {e!r}')
                continue

            with file:
                for pageNum in range(len(file)):
                    page = file[pageNum]
                    text = page.get_text()
                    if re.search(regexPattern, text):
                        subResult = pdfFileName, pageNum + 1
                        result.append(subResult)
                        break
        return result