from enum import unique
from io import StringIO
import os
from typing_extensions import final

from underthesea import word_tokenize
from underthesea import sent_tokenize

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
    with open('specialChar.txt','r',encoding='utf-8') as f:
        specialChar=f.read().split()
    for char in specialChar:
        input_str=input_str.replace(char,'')
    return input_str

def read_allTextFile():
    text=''
    for folder in os.listdir('data'):
        for textFile in os.listdir('data/'+folder):
            with open('data/'+folder+'/'+textFile,'r',encoding='utf-8') as f:
                temp=f.read()
                text+=temp+' '
    return text

def get_uniqueList(list_input):
    unique=[]
    for string in list_input:
        if string not in unique:
            unique.append(string)
    return unique


def generate_vocab(unique:bool):    
    document= read_allTextFile()
    document_array=document.split('.')
    doc_array=[]

    for i in range(len(document_array)):
        if document_array[i]!='' and not document_array[i].isspace():
            doc_array.append(remove_speChar(document_array[i]))

    for i in range (len(doc_array)):
        temp=word_tokenize(doc_array[i],format='text')
        doc_array[i]=temp.lower()

    temp_vocab=[]
    for i in range(len(doc_array)):
        temp=doc_array[i].split()
        temp_vocab.extend(temp)
    
    final_vocal=[]
    with open('dic.txt','r',encoding='utf-8') as f:
        temp_dict=f.read()
        underthesea_words=temp_dict.split('\n')

# 2 MODE -> TRUE : unique 
#       -> FALSE : simple
    if unique == True:
        unique_vocab=get_uniqueList(temp_vocab)
        for element in unique_vocab:
            if element in underthesea_words:
                final_vocal.append(element)
        return final_vocal
    else:
        for element in temp_vocab:
            if element in underthesea_words:
                final_vocal.append(element)
        return final_vocal

