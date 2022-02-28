from io import StringIO
import os
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import TextConverter


def convert_pdf_to_string(file_path):
    output_string = StringIO()
    with open(file_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return(output_string.getvalue())


def convert_title_to_filename(title):
    filename = title.lower()
    filename = filename.replace(' ', '_')
    return filename


def split_to_title_and_pagenum(table_of_contents_entry):
    title_and_pagenum = table_of_contents_entry.strip()
    title = None
    pagenum = None
    if len(title_and_pagenum) > 0:
        if title_and_pagenum[-1].isdigit():
            i = -2
            while title_and_pagenum[i].isdigit():
                i -= 1
            title = title_and_pagenum[:i].strip()
            pagenum = int(title_and_pagenum[i:].strip())
    return title, pagenum


def remove_speChar(input_str):
    with open('specialChar.txt', 'r', encoding='utf-8') as f:
        specialChar = f.read().split()
    for char in specialChar:
        input_str = input_str.replace(char, ' ')
    return input_str


def renderPdf(writer, reader):
    for page in range(2, reader.numPages):
        writer.addPage(reader.getPage(page))

    pdfFile_temp = "temp.pdf"
    with open(pdfFile_temp, 'wb') as temp:
        writer.write(temp)
    text = convert_pdf_to_string(pdfFile_temp)
    os.remove(pdfFile_temp)
    text = remove_speChar(text)
    for char in text:
        if char.isdigit():
            text = text.replace(char, '')
    with open('input\doc.txt', 'w', encoding='utf-8') as textFile:
        textFile.write(' '.join(text.strip().split()))
