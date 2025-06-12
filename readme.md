## Fast PDF Reader
Assume that you have 300 PDF files in one folder and you want to find the one with API documentation. The names of the files aren't meaningful, so you either have to find the file manually or you can use this tool.

This simple program search given patter (regex) in PDF files in chosen folder. The results are displayed in a table. You can click a row to open the file.

## How to install
1. Install python - tool was made with `python 3.12.9`.
2. Install libraries with command `pip install -r requirements.txt`
3. Run `main.pyw`

Windows users can use the provided bat scripts:
- `install libraries.bat` creates virtual environment and install needed libraries
- `run.bat` launches the program