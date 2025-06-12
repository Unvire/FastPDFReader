import pytest
import fastPdfSearcher
import logging

logger = logging.getLogger(__name__)

def test__splitFilesListToChunks():
    instance = fastPdfSearcher.FastPdfSearcher()
    data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    
    expected = [[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24], [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]]
    result = instance._splitFilesListToChunks(data, 2)
    assert expected == result

    expected = [[0, 3, 6, 9, 12, 15, 18, 21, 24], [1, 4, 7, 10, 13, 16, 19, 22, 25], [2, 5, 8, 11, 14, 17, 20, 23]]
    result = instance._splitFilesListToChunks(data, 3)

    expected = [[0, 10, 20], [1, 11, 21], [2, 12, 22], [3, 13, 23], [4, 14, 24], [5, 15, 25], [6, 16], [7, 17], [8, 18], [9, 19]]
    result = instance._splitFilesListToChunks(data, 10)
    assert expected == result

    expected = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]]
    result = instance._splitFilesListToChunks(data, 1)
    assert expected == result
    