import chromadb, os
from chromadb.config import Settings

from PyPDF2 import PdfReader
import re


extraPdfs = [ ]

mds = []
docs = []
metas = []


def make(LIB_PATH):
    ids = []
    for pdf in os.listdir(LIB_PATH)+extraPdfs:
        if not pdf.endswith(".pdf"):
            continue
        with open(os.path.join(LIB_PATH,pdf), "rb") as file:
            content = PdfReader(file)
            for p, page in enumerate(content.pages):
                metas.append({"page": p+1, "pdf": pdf})
                docs.append(page.extract_text())

                ids.append(f"page - {p+1} : {pdf}")


    return [docs,metas,ids]


