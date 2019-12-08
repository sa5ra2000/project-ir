import collections
import math
import random
import numpy as np

path_dictionary = {'d1': '1.txt',
                   'd2': '2.txt',
                   'd3': '3.txt',
                   'd4': '4.txt',
                   'd5': '5.txt'
                  }

def get_term_freq(path_dic):
    term_freq = {}
    for key in path_dic:
        filename = path_dic[key]
        file = open(filename,'a+')
        file = open(filename, 'r')
        print(file)
        chars = file.read().split(' ')
        dic = {}
        for i in range(len(chars)):
            char = chars[i]
            if(char.isnumeric()):
                continue
            if char == '':
                continue
            if char not in dic:
                dic[char] = 1
            else:
                dic[char] = dic[char] + 1
        term_freq[key] = dic
    # print(term_freq)
    return term_freq


def get_normalized_term_freq(path_dic):
    docs_term_freq = get_term_freq(path_dic)
    docs_norm_term_freq = {}
    max = 0
    for doc in docs_term_freq:
        term_freq = docs_term_freq[doc]
        norm_term_freq = {}
        for term in term_freq:
            if (term_freq[term] > max):
                max = term_freq[term]
        for term in term_freq:
            norm_term_freq[term] = term_freq[term] / max
        docs_norm_term_freq[doc] = norm_term_freq
    # print(docs_norm_term_freq)
    return docs_norm_term_freq


def get_df(path_dic):
    docs_term_freq = get_term_freq(path_dic)
    df = {}
    for doc in docs_term_freq:
        chars = docs_term_freq[doc].keys()
        for char in chars:
            if char not in df:
                df[char] = 1
            else:
                df[char] = df[char] + 1
    # print(df)
    return df


def get_idf(path_dic):
    df = get_df(path_dic)
    idf = {}
    for char in df:
        numberOfDocs = df[char]
        idf[char] = math.log2(len(path_dic) / numberOfDocs)
    # print(idf)
    return idf


def get_tf_idf_weights(path_dic):
    ntf = get_normalized_term_freq(path_dic)
    idf = get_idf(path_dic)
    tf_idf_w = {}
    for doc in ntf:
        ntf_dic = ntf[doc]
        ntf_idf_dic = {}
        for char in ntf_dic:
            tfij = ntf_dic[char]
            idfi = idf[char]
            ntf_idf_dic[char] = tfij * idfi
        tf_idf_w[doc] = ntf_idf_dic
    # print(tf_idf_w)
    return tf_idf_w


def save_input(input):
    input = input.split(' ')
    text = ''
    for word in input:
        text += word
    doc = ''
    for char in text:
        doc = doc + char + ' '
    file = open('input.txt', 'w')
    file.write(doc)
    path_dictionary['query'] = 'input.txt'


def get_sim(d, q):
    sum = 0
    for char in q:
        wq = q[char]
        wd = 0
        if char in d:
            wd = d[char]
        sum = sum + (wq * wd)
    return sum


def get_cosSim_dic(path_dic):
    cosSim_dic = {}
    weights = get_tf_idf_weights(path_dic)
    qw = weights['query']
    query_sum_weights = 0
    for w in qw:
        query_sum_weights += qw[w] * qw[w]

    for doc in path_dic:
        if doc != 'query':
            dw = weights[doc]
            doc_sum_weights = 0
            for w in dw:
                if w in qw:
                    doc_sum_weights += dw[w] * dw[w]

            sim = get_sim(dw,qw)
            y= math.sqrt(query_sum_weights * doc_sum_weights)
            if not y ==0 :
                cosSim = sim/y
            else:
                cosSim=0
            cosSim_dic[doc] = cosSim

    return cosSim_dic

############################################################################################
#PROJECT 1 FUNCTIONS END HERE
############################################################################################

def generate_Random(path_dictionary) :
    allchars="QWERTYUIOPASDFGHJKLZXCVBNM12345"
    for i in path_dictionary :
        filename=path_dictionary[i]
        file=open(filename,'w')
        for j in range(10):
            x=random.randint(0,30)
            char=allchars[x]
            file.write(str(char)+' ')
        file.close()

def get_adj_mat(path_dic):
    mat = np.zeros((5, 5), dtype=int)
    index = 0
    for file in path_dic:
        index = index + 1
        textFile = open(path_dic[file], 'r')
        chars = textFile.read().split(' ')
        for char in chars:
            if(char.isnumeric()):
                mat[index - 1][int(char) - 1] = 1
        mat[index - 1][index - 1] = 0
    return mat

def calc_auth_hub(mat):
    matTr = mat.transpose()
    hub = np.ones(5, dtype=int)
    for i in range(20):
        a = np.dot(matTr,hub)
        nor = np.linalg.norm(a)
        a = a / nor
        hub = np.dot(mat,a)
        nor = np.linalg.norm(hub)
        hub = hub / nor
    return {'auth': a, 'hub': hub}

def sort_auth_hub(authhub):
    auth = authhub['auth']
    hub = authhub['hub']
    authlist = []
    hublist = []
    for i in range(5):
        ind = i + 1
        file = "D"+str(ind)
        authlist.append((round(auth[i], 2), file))
        hublist.append((round(hub[i], 2), file))
    authlist.sort(reverse=True)
    hublist.sort(reverse=True)
    return {'auth': authlist,
            'hub': hublist}

print(sort_auth_hub(calc_auth_hub(get_adj_mat(path_dictionary))))

############################################################################################
#PROJECT 2 FUNCTIONS ENDS HERE
############################################################################################

def main(query):
    generate_Random(path_dictionary)
    save_input(query)
    x = get_cosSim_dic(path_dictionary)
    x = sorted(x.items(), key=lambda kv: kv[1], reverse=True)
    # print(x)
    dict_out = {}
    for i in x:
        dict_out[i[0]] = i[1]

    return dict_out

from flask import Flask, render_template, url_for, flash, redirect, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', show=False)


@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    if request.method == 'POST':
        text = str(request.form['text'])
        if text == "":
            return render_template('home.html', list=None, show=False)
        return render_template('home.html', list=main(text), show=True)
    return render_template('home.html', show=False)


app.debug = True
app.run()
