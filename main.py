from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
import data_func
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vncorenlp import VnCoreNLP
import os
import pandas as pd
import mysql.connector

cnx = mysql.connector.connect(user = 'localhost',
                              password = 'Hung2001@',
                              host = '127.0.0.1',
                              database = 'plagiarism')


# IN :
# Step 1 : Choose subject
# Step 2 : Choose input mode
# - StudentMode -> Update One file
# - TeacherMode -> Update One/Many file
# Step 3 : Update pdf file/files

# OUT :
# Student mode : return score
# Teacher mode : return excel file

class Document:
    def __init__(self, subject, mode, directory):
        self.subject = subject
        self.mode = mode
        self.directory = directory

    def convertPDF2Text(self):
        if self.mode == 2:
            reader = PdfFileReader(self.directory)
            writer = PdfFileWriter()
            for page in range(2, reader.numPages):
                writer.addPage(reader.getPage(page))

            file_temp = 'temp.pdf'
            with open(file_temp, 'wb') as temp:
                writer.write(temp)
            text = data_func.convert_pdf_to_string(file_temp)
            os.remove(file_temp)

            text = data_func.remove_speChar(text)

            for char in text:
                if char.isdigit():
                    text = text.replace(char, '')
            text = text.strip()
            with open('input\doc.txt', 'w', encoding='utf-8') as textFile:
                textFile.write(' '.join(text.split()))

        elif self.mode == 1:
            for file in os.listdir(self.directory):
                if file.endswith('.pdf'):
                    reader = PdfFileReader(self.directory+'/'+file)
                    writer = PdfFileWriter()

                    for page in range(2, reader.numPages):
                        writer.addPage(reader.getPage(page))

                    file_temp = 'temp.pdf'
                    with open(file_temp, 'wb') as temp:
                        writer.write(temp)
                    text = data_func.convert_pdf_to_string(file_temp)
                    os.remove(file_temp)

                    text = data_func.remove_speChar(text)
                    for char in text:
                        if char.isdigit():
                            text = text.replace(char, '')
                    text = text.strip()
                    with open('input/'+file[:-4]+'.txt', 'w', encoding='utf-8') as textFile:
                        textFile.write(' '.join(text.split()))

    def checker(self):
        annotator = VnCoreNLP(address="http://127.0.0.1", port=9000)
        corpus = []
        plain_path = 'input/'
        input_files = [file for file in os.listdir(
            plain_path) if file.endswith('.txt')]

        for input_file in input_files:
            with open(plain_path+input_file, 'r', encoding='utf-8') as fr:
                file_name = input_file
                file_content = fr.read()
                corpus.append((file_name, file_content))
        doc_names, doc_data = zip(*corpus)

        for single_doc in doc_data:
            # output: word tokenized array
            temp = annotator.tokenize(single_doc)
            # đưa về raw document
            for ele in temp:
                data_raw = ' '.join(ele)
            single_doc = data_raw.lower()
        vectorizer = CountVectorizer()
        # return a term-document matrix with doc_data as input
        # X: array, [n_samples, n_featrues]
        document_term_matrix = vectorizer.fit_transform(doc_data)

        tf_enable = True
        if(tf_enable):
            tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
            tfidf_transformer.fit(document_term_matrix)
            idf = tfidf_transformer.idf_

            # print idf values
            df_idf = pd.DataFrame(
                tfidf_transformer.idf_, index=vectorizer.get_feature_names(), columns=["idf_weights"])

            # sort asc idf
            df_idf.sort_values(by=['idf_weights'])
            # print(df_idf)

            tf_idf_vector = tfidf_transformer.transform(document_term_matrix)

            df = pd.DataFrame(tf_idf_vector.T.todense(
            ), index=vectorizer.get_feature_names(), columns=doc_names)
            print(df)

            cosine_matrix = cosine_similarity(tf_idf_vector)
            df = pd.DataFrame(data=cosine_matrix,
                              columns=doc_names,
                              index=doc_names)
            print(df)
            # returns full list of tokenized words
            tokenized_words = vectorizer.get_feature_names()
            # output pandas table document_term_matrix
            df = pd.DataFrame(data=document_term_matrix.toarray(),
                              columns=tokenized_words,
                              index=doc_names)
            cosine_matrix = cosine_similarity(document_term_matrix)

            df = pd.DataFrame(data=cosine_matrix,
                              columns=doc_names,
                              index=doc_names)

            print(df)


def main():
    directory_input = Document(1, 'sub1', 'D:/input_plagiarism/')
    directory_input.checker()


if __name__ == "__main__":
    main()
