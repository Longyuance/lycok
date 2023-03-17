f=open("tcpl5.txt",'r')
tcshuju=f.read().splitlines()
for cc in tcshuju:
    if cc=='':
        tcshuju.remove(cc)
print(tcshuju)
print(len(tcshuju))
# newtcshuju=tcshuju[0:100]
# print(newtcshuju)
# fw=open('tcnew.txt','w')
# sj: str
# for sj in newtcshuju:
#     fw.write(sj+'\n')

