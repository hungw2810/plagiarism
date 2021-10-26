from io import StringIO
import os

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

def dictionary(subject):
    sentences=''
    subject_dir='data/'+subject
    for text_file in os.listdir(subject_dir):
        with open(subject_dir+'/'+text_file,'r',encoding='utf-8') as f:
            sentences+=f.read()
    sentences=word_tokenize(sentences,format='text')
    words=sentences.split()

    vocab=[]
    [vocab.append(words[x]) for x in range(len(words)) if not words[x].__contains__('.')]

    vocab=list(dict.fromkeys(vocab))
    for i in range(len(vocab)):
        vocab[i]=vocab[i].lower()
    return vocab

def remove_speChar(input_str):
    with open('stopwords.txt','r',encoding='utf-8') as f:
        stopwords=f.read().split()
        # speChar=speChar.replace('\t','')
        # speChar=speChar.split('\n')
    input_str=word_tokenize(input_str,format="text")
    textquerry=input_str.split()
    resultword=[word for word in textquerry if word.lower() not in stopwords]
    result=' '.join(resultword)
    return result.lower()




