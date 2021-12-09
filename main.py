from unicodedata import name
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
import os
import data_func
from underthesea import word_tokenize
from underthesea import sent_tokenize
import re

class document:
    #attribute

# mode 2 -> exact direct pdf file   -- accpunt free
# mode 1 -> directory of folder contain pdf files       --acount premium

    def __init__(self,mode,sub,direct):
        self.mode=mode
        self.subject=sub
        self.directory=direct

    def convertPDF2Text(self):
        if self.mode==2:
            reader=PdfFileReader(self.directory)
            file_pages=reader.numPages
            writer=PdfFileWriter()

            for page in range(2,file_pages):
                writer.addPage(reader.getPage(page))

            file_temp ='temp.pdf'
            with open(file_temp,'wb') as temp:
                writer.write(temp)           
            text = data_func.convert_pdf_to_string(file_temp)
            os.remove(file_temp)

            text=data_func.remove_speChar(text)
            
            for char in text:
                if char.isdigit():
                    text=text.replace(char,'')
            text=text.strip()
            with open('input\doc.txt','w', encoding='utf-8') as textFile:
                textFile.write(' '.join(text.split()))
        
        elif self.mode==1:
            for file in os.listdir(self.directory):
                if file.endswith('.pdf'):
                    reader=PdfFileReader(self.directory+'/'+file)
                    file_pages=reader.numPages
                    writer=PdfFileWriter()

                    for page in range(2,file_pages):
                        writer.addPage(reader.getPage(page))

                    file_temp ='temp.pdf'
                    with open(file_temp,'wb') as temp:
                        writer.write(temp)           
                    text = data_func.convert_pdf_to_string(file_temp)
                    os.remove(file_temp)

                    text=data_func.remove_speChar(text)
                    for char in text:
                        if char.isdigit():
                            text=text.replace(char,'')
                    text=text.strip()
                    with open('input/'+file[:-4]+'.txt','w', encoding='utf-8') as textFile:
                        textFile.write(' '.join(text.split()))
## chưa xong
    def split_to_array(self):
        for txtFile in os.listdir('input'):
            with open('input/'+txtFile,'r',encoding='utf-8') as fr:
                document=fr.read()
                sent_array=sent_tokenize(document)
            with open('input/'+txtFile,'w',encoding='utf-8') as fw:
                for item in sent_array:
                    if len(item)>=6:
                        fw.write(item+"\n")  

def main():
    print("Welcome bruh!!!")
    print("----SELECT MODE----")
    print("1--premium")
    print("2--free")
    mode=int(input())
    print("----ENTER SUBJECT----")
    subject=input()
    if mode == 1:
        print("----ENTER directory contain documents----")
        directory=input()
    else:
        print("----ENTER exact directory of document----")
        directory=input()

    obj=document(mode,subject,directory)
    print("----WORKING----")
    obj.convertPDF2Text()
    obj.split_to_array()
    print("----FINISHED----")

if __name__ == "__main__":
    main()
