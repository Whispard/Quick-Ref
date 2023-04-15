import subprocess, os

PDF_READERS = {
    "Sumatra": "Path for Sumatra reader",
    "Adobe": r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
}

# Select One From Above
READER_TO_USE = None
ENABLE_HIGHLIGHT = True


def open_reader(reader, pdf_path, page, search=""):
    if not reader in PDF_READERS.keys():
        print("Invalid Reader")
        return
    readerPath = PDF_READERS[reader]
    if reader == "Adobe":
        if search == "":
            args = [readerPath, '/A', f"page={page}", pdf_path]
        else:
            args = [readerPath, '/A', f"page={page}&search={search}", pdf_path]


    elif reader == "Sumatra":
        if search == "":
            args = [readerPath, '-page', f"{page}", pdf_path]
        else:
            args = [readerPath, '-page', f"{page}", '-search', search, pdf_path]

    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)

    print(f"OPENED {reader} with pdf: {pdf_path} at page: {page} and search: {search}")
    # p.wait()
