def remove_stopwords(input_string):
    with open ('test.txt',mode='r',encoding='utf-8') as f:
        stopwords=f.read()
        stopwords=stopwords.replace('\t','')
        stopwords=stopwords.split('\n')
    for i in range(len(stopwords)):
        input_string=input_string.replace(stopwords[i],'')
    return input_string.strip()



input_string=("hôm nay thứ hai đó nấy ai anh ấy")
output=remove_stopwords(input_string)
print(output)


# with open ('D:/Plagiarism/stopwords.txt',mode='r',encoding='utf-8') as f:
#         stopwords=f.read()
#         stopwords=stopwords.replace('\t','')
#         stopwords=stopwords.split('\n')
# print(stopwords)