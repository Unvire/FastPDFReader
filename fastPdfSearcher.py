import os
from multiprocessing import Pool
import fitz
import time

class FastPdfSearcher:
    def __init__(self):
        self.timeStamp = None
        
    
    def _elapsedTime(self) -> float:
        return time.time() - self.timeStamp


if __name__ == '__main__':
    pass