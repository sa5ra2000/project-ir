import random

path_dic={'D1':"D1.txt",'D2':"D2.txt",'D3':"D3.txt"}

#putting all words of the collection docs in one dictionary
def GetChars (path) :
    chars_dic ={}
    for key in path :
        f = open(path[key], "r")
        x = f.read()
        x = x.replace(" ", "")
        for i in x :
            chars_dic[i]=0
    #print(chars_dic)
    return chars_dic

#calculate the length of all words in the document..
def calclen(path) :
    f = open(path, "r")
    x = f.read()
    x = x.replace(" ", "")
    return len(x)

#calculate the freq. of every word in the doc..
def repeat(path) :
    f = open(path, "r")
    x = f.read()
    x = x.replace(" ", "")
    d = {}
    for i in range(0, len(x)):
        char = x[i]
        if char in d:
            d[char] += 1
        else:
            d[char] = 1
    return d

#generate random chars in documents...
allchars="QWERTYUIOPASDFGHJKLZXCVBNM"
for i in path_dic :
    filename=path_dic[i]
    file=open(filename,'w')
    for j in range(10):
        x=random.randint(0,25)
        char=allchars[x]
        file.write(str(char)+' ')
    file.close()

#get dictionary of all words in the collection of docs
chars=GetChars(path_dic)

#get dictionary of freq. of words
file_dic={}
for i in path_dic:
    y=repeat(path_dic[i])
    z=calclen(path_dic[i])
    for j in y :
        y[j]=round(y[j]/z,2)
    file_dic[i] = y

#if there is word not in in the doc
#we put it in the dic with value zero...
uniqchars = chars.keys()
for char in uniqchars:
    for d in file_dic:
        dic = file_dic[d]
        if char not in dic:
            dic[char] = 0

#take the query from the user as an input..
inpdic={}
for i in range(3):
    x=input("enter key ?")
    y=input("enter value ?")
    inpdic[x] = float(y)

print(inpdic)
print(file_dic)

score =0
ScoreDic={}

#calculate the scores of every document
#and return the scores in dictionary
for j in file_dic :
    dic2 = file_dic[j]
    # print(file_dic[j])
    for i in inpdic :
        if i in dic2 :
            score = score + (inpdic[i]*dic2[i])
            ScoreDic[j] = score
    score=0

max=-999
name =""
for i in ScoreDic :
    if max<ScoreDic[i] :
        max=ScoreDic[i]
        name =i

print(ScoreDic)
print("The most similar document is :",name,"with value :",max)