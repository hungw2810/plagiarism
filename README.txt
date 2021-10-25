
## RUN MAIN
# for file in os.listdir("oldPDF"):
#     if file.endswith('.pdf'):
#         if not os.path.exists('newPDF\\'+file[:-4]):
#             convertPDF2Text(file)



## stop word

# improve 1:

# tinh ra n similarity score
# tinh ra similarity score chung
# improve 2:
# trich ra ten rieng, so sanh xem ten rieng co trung lap nhieu khong
# VnCoreNLP, Underthesea
#
# chia ra topic, chi so sanh trong topic day
# to chuc du lieu: ma lop, ma mon hoc, ten mon hoc, giang vien, nam hoc, hoc ky, ...

# production
# sinh vien: up 1 file len de check dao van -> bat nhap mon gi -> so sanh voi document cua mon do (vi du 200 docs) -> chi can so sanh 200 lan -> thong bao ket qua %
# giang vien: thuong la upload ca folder -> zip lai -> check lan luot tung bai -> return ket qua similarity cua nhung bai co score cao
# admin: quan ly du lieu

# tu dong nghia, paraphrase
# tim hieu ly thuyet plagiarism
# thu vien synonym

# check version cua file sinh vien up len
# to chuc du lieu nhu the nao de luu duoc nhieu phien ban
# caching de tang toc do xu ly



