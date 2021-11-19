from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
import os
import data_func
from underthesea import word_tokenize
from underthesea import sent_tokenize
import re

class Subject:
    def __init__(self,id_subject) -> None:
        self.id_subject=id_subject

    def convertPDF2Text(self,pdf_file):
        reader=PdfFileReader('pdf_file/'+self.id_subject+'/'+pdf_file)
        file_pages=reader.numPages
        writer=PdfFileWriter()
        
        for page in range(1,file_pages):
            writer.addPage(reader.getPage(page))

        output_file ='pdf_file/'+self.id_subject+'/temp.pdf'
        with open(output_file,'wb') as output:
            writer.write(output)           
        text = data_func.convert_pdf_to_string(output_file)
        os.remove(output_file)

        # remove punctuation and stopwords
        text=data_func.remove_speChar(text)

        ## remove all number
        for char in text:
            if char.isdigit():
                text=text.replace(char,'')

        text=text.strip()
        
        if not os.path.exists('data/'+self.id_subject):
            os.makedirs('data/'+self.id_subject)

        with open("data/"+self.id_subject+'/'+pdf_file[:-4]+".txt",'w', encoding='utf-8') as textFile:
            textFile.write(' '.join(text.split()))

def main(id_subject):
    subject=Subject(id_subject)
    for file in os.listdir('pdf_file/'+id_subject):
        if file.endswith('.pdf') and file != 'temp.pdf':
            subject.convertPDF2Text(file)

# print('WORKING.....')
# main('sub1')
# print("FINISHED!!")
