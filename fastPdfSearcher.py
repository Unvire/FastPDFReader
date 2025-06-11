import os
import fitz
import time

import multiprocessing
from multiprocessing import Pool

class FastPdfSearcher:
    def __init__(self):
        self.timeStamp = None

    
    def _elapsedTime(self) -> float:
        return time.time() - self.timeStamp
    
    def _calculateNumberOfProcesses(self) -> int:
        return multiprocessing.cpu_count()
    
    def _splitFilesListToChunks(self, pdfFileNames:list[str], numOfChunks:int) -> list[list[str]]:
        result = [[] for _ in range(numOfChunks)]
        fileNamesCopy = pdfFileNames[:]
        while fileNamesCopy:
            chunk = result.pop(0)
            chunk.append(fileNamesCopy.pop(0))
            result.append(chunk)
        return result

if __name__ == '__main__':
    instance = FastPdfSearcher()