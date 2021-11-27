import data_func
import cal_func
import numpy as np
from numpy import dot
from numpy.linalg import norm

idf=[]

vector1=[]
vector2=[]
vector3=[]
vector4=[]
list_sent=[]
#base
#sent 1= cơ_sở nghiên_cứu khoa_học
sent1=data_func.preProcessSent("Hà Nội đẹp nhất về đêm") #count word = 2
#target
sent2=data_func.preProcessSent("Thời điểm đẹp nhất là đêm")
sent3=data_func.preProcessSent("Hà Nội mùa này là mùa đẹp nhất")
sent4=data_func.preProcessSent("đêm đẹp nhất về Hà Nội")


list_sent.append(sent2)
list_sent.append(sent3)
list_sent.append(sent4)

for word in sent1:
    vector1.append(cal_func.cal_TF(word,sent1))
    vector2.append(cal_func.cal_TF(word,sent2))
    vector3.append(cal_func.cal_TF(word,sent3))
    vector4.append(cal_func.cal_TF(word,sent4))
    
#calculate idf base on sent1
for word in sent1:
    idf.append(cal_func.cal_IDF(word,list_sent))

vector1=np.multiply(vector1,idf)
vector2=np.multiply(vector2,idf)
vector3=np.multiply(vector3,idf)
vector4=np.multiply(vector4,idf)

print(dot(vector1, vector2)/(norm(vector1)*norm(vector2)))
print(dot(vector1, vector3)/(norm(vector1)*norm(vector3)))
print(dot(vector1, vector4)/(norm(vector1)*norm(vector4)))



