from enum import unique
from io import StringIO
import os
import math
from typing_extensions import final
import pandas as pd
from underthesea import word_tokenize
from underthesea import sent_tokenize

from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import TextConverter
from underthesea.pipeline.word_tokenize.regex_tokenize import tokenize


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
        input_str=input_str.replace(char,' ')
    return input_str

def preProcessSent(sentence):
    output_array=[]
    tokenized_sent=word_tokenize(sentence,format="text").lower()
    word_array=tokenized_sent.split()
    with open('vietnamese_dictionary.txt','r',encoding="utf-8") as f:
        dictionary=f.read().split('\n')
    for word in word_array:
        if word in dictionary:
            output_array.append(word)
    return output_array

def cal_TF(word_input,word_array):
    occur=word_array.count(word_input)
    return occur/len(word_array)

def cal_IDF(word_input,list_wordArray):
    count=0
    for wordArray in list_wordArray:
        if wordArray.count(word_input) > 0:
            count+=1
    return math.log(len(list_wordArray)/count)