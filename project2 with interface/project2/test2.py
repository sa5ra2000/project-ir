import collections
import math

path_dictionary = {'d1': 'd1.txt',
                   'd2': 'd2.txt',
                   'd3': 'd3.txt',
                   'd4': 'd4.txt',
                   'd5': 'd5.txt',
                   }


def get_term_freq(path_dic):
    term_freq = {}
    for key in path_dic:
        filename = path_dic[key]
        file = open(filename, 'r')
        chars = file.read().split(' ')
        dic = {}
        for i in range(len(chars)):
            char = chars[i]
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

            sim = get_sim(dw, qw)
            cosSim = sim / math.sqrt(query_sum_weights * doc_sum_weights)
            cosSim_dic[doc] = cosSim
    return cosSim_dic


def main():
    save_input('my name is mohammad')
    x = get_cosSim_dic(path_dictionary)
    x = sorted(x.items(), key=lambda kv: kv[1], reverse=True)
    # print(x)
    dict_out = {}
    for i in x:
        dict_out[i[0]] = i[1]
    return dict_out
# print(dict_out)
# get_tf_idf_weights(path_dictionary)
# get_idf(path_dictionary)
# get_df(path_dictionary)
# get_normalized_term_freq(path_dictionary)
# get_term_freq(path_dictionary)
