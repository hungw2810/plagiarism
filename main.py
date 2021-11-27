from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
import os
import data_func
from underthesea import word_tokenize
from underthesea import sent_tokenize
import re

def convertPDF2Text(directory):
    for file in os.listdir(directory):
        if file.endswith('.pdf') and file != 'temp.pdf':
            direcPDF=directory+'/'+file
            reader=PdfFileReader(direcPDF)
            file_pages=reader.numPages
            writer=PdfFileWriter()
            
            for page in range(1,file_pages):
                writer.addPage(reader.getPage(page))

            output_file =directory+'/temp.pdf'
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
            txtDirectory=directory+'/'+ file[:-4]+".txt"
            with open(txtDirectory,'w', encoding='utf-8') as textFile:
                textFile.write(' '.join(text.split()))


#### chua xong#####
def tokenize(directory):
    sent_array=[]
    for file in os.listdir(directory):
        if file.endswith('.txt'):
            with open(directory+'/'+file,'r',encoding='utf-8') as textFile:
                document=textFile.read()   
            sentences=document.split('.')
            for i in range(len(sentences)):
                if sentences[i] != '' and not sentences[i].isspace():
                    sent_array.append(data_func.remove_speChar(sentences[i]))
            
            for i in range (len(sent_array)):
                temp=word_tokenize(sent_array[i],format='text')
                sent_array[i]=temp.lower()
            
            with open(directory+'/'+file,'w',encoding='utf-8') as textFile:
                for sent in sent_array:
                    textFile.write(sent+'\n')





print('Enter directory contain pdf input')
directory=input()
print('Working')
convertPDF2Text(directory)
tokenize(directory)
print('Finished')
