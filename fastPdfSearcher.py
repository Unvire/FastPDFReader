import os, time, re, multiprocessing
import fitz

class FastPdfSearcher:
    def __init__(self):
        self.timeStamp = None

    def searchPDFs(self, folderPath:str, pdfFileNames:list[str], pattern:str) -> list[tuple[str, int]]:
        numOfProcesses = self._numberOfProcesses()
        pdfFileNamesChunked = self._splitFilesListToChunks(pdfFileNames, numOfProcesses)

        processArguments = [(folderPath, chunk, pattern) for chunk in pdfFileNamesChunked]
        with multiprocessing.Pool(processes=numOfProcesses) as pool:
            results = pool.map(FastPdfSearcher.searchPdfChunk, processArguments)
        
        return self._flattenSearchResult(results)
    
    def _elapsedTime(self) -> float:
        return time.time() - self.timeStamp
    
    def _numberOfProcesses(self) -> int:
        return multiprocessing.cpu_count()
    
    def _splitFilesListToChunks(self, pdfFileNames:list[str], numOfChunks:int) -> list[list[str]]:
        result = [[] for _ in range(numOfChunks)]
        fileNamesCopy = pdfFileNames[:]
        while fileNamesCopy:
            chunk = result.pop(0)
            chunk.append(fileNamesCopy.pop(0))
            result.append(chunk)
        return result
    
    def _flattenSearchResult(self, searchResults:list[list[tuple[str, int]]]) -> list[tuple[str, int]]:
        resultFlattened = []
        for chunkResult in searchResults:
            if not chunkResult:
                continue
            resultFlattened += chunkResult
        return resultFlattened

    @staticmethod
    def searchPdfChunk(processArguments) -> list[tuple[str, int]]:
        folderPath, pdfFileNames, regexPattern = processArguments
        result = []
        for pdfFileName in pdfFileNames:
            pdfFilePath = os.path.join(folderPath, pdfFileName)
            try:
                file = fitz.open(pdfFilePath)
            except Exception as e:
                print(f"Błąd przy otwieraniu {pdfFilePath}: {e!r}")
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

if __name__ == '__main__':
    path = r'B:\PROJECTS_U62\ENERGY\ENEL\2. ENDESA\4. Nexy - M\01_Requirements\01_Customer\00_DMI\DMI NEXY-M LITE\DMIs'
    pdfFiles = [name for name in os.listdir(path) if name.lower().endswith('.pdf')]
    pattern = 'STANDARD'
    
    instance = FastPdfSearcher()
    result = instance.searchPDFs(path, pdfFiles, pattern)
    print(result)