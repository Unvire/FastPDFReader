import os
from multiprocessing import Pool
import fitz
import time


def find_word_in_pdf(args):
    file_path, word = args
    try:
        with fitz.open(file_path) as doc:
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if word.lower() in text.lower():
                    return file_path, page_num + 1
    except Exception as e:
        return file_path, f"Error: {e}"

def search_for_flag_in_pdfs(folder_path, word, processes=None):
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]

    with Pool(processes=processes) as pool:
        results = pool.map(find_word_in_pdf, [(file_path, word) for file_path in file_paths])

    total_files_processed = len(file_paths)  # Liczba przetworzonych plików

    for result in results:
        if result is not None:
            file_path, outcome = result
            if isinstance(outcome, int):
                print(f"'{word}' found in {file_path} on page {outcome}")
            else:
                print(f"{file_path}: {outcome}")

    print(f"Liczba przetworzonych plików: {total_files_processed}")

if __name__ == '__main__':
    start_time = time.time()
    search_for_flag_in_pdfs(r'C:\SPEA\Documentation\3030 IL - Manuals V5.10.5', 'OBJECT')
    elapsed_time = time.time() - start_time
    print(f"Czas wykonania całego skryptu: {elapsed_time} sekund")