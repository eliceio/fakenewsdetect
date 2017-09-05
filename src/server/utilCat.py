"""
util for predCat.py
~08.25.2017
Stackcat
"""
from csv import DictReader
from csv import DictWriter
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
import pandas as pd
from gensim import models
from sklearn.externals import joblib
import re

label_ref = {'agree': 0, 'disagree': 1, 'discuss': 2, 'unrelated': 3}
label_ref_rev = {0: 'agree', 1: 'disagree', 2: 'discuss', 3: 'unrelated'}
stop_words = [
       'a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'ain', 'all', 'almost', 'alone', 'along',         'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another',
        'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'aren', 'around', 'as', 'at', 'back', 'be',
        'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below',
        'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can', 'co', 'con', 'could',
        'couldn', 'cry', 'd', 'de', 'describe', 'detail', 'did', 'didn', 'do', 'does', 'doesn', 'doing', 'don', 'done',          'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc',
        'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fifty', 'fill', 'find',
        'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further',
         'get', 'give', 'go', 'had', 'hadn', 'has', 'hasn', 'have', 'haven', 'having', 'he', 'hence', 'her', 'here',          'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred',
         'i', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 'isn', 'it', 'its', 'itself', 'just', 'keep',
         'last', 'latter', 'latterly', 'least', 'less', 'll', 'ltd', 'm', 'ma', 'made', 'many', 'may', 'me', 'meanwhile',
         'might', 'mightn', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'mustn', 'my',          'myself', 'name', 'namely', 'needn', 'neither', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'nor', 'not', 'now',
         'nowhere', 'o', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our',
         'ours', 'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 's', 'same',
         'see', 'serious', 'several', 'shan', 'she', 'should', 'shouldn', 'show', 'side', 'since', 'sincere', 'six', 'sixty',          'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 't',          'take', 'ten', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter',          'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thick', 'thin', 'third', 'this', 'those', 'though',
         'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty',
         'two', 'un', 'under', 'until', 'up', 'upon', 'us', 've', 'very', 'via', 'was', 'wasn', 'we', 'well', 'were', 'weren',          'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon',          'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with',          'within', 'without', 'won', 'would', 'wouldn', 'y', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves'
        ]
w2v_size = 300

# get cosine similarity
def get_w2v_cs(model, head, body):
    toks_head = tokenize(head)
    toks_body = tokenize(body)

    vec_head = sum(np.array([model.wv[h] for h in toks_head if h in model.wv]))
    vec_body = sum(np.array([model.wv[b] for b in toks_body if b in model.wv]))
    if isinstance(vec_head, int) and vec_head == 0:
        vec_head = np.zeros((w2v_size,))
        if isinstance(vec_body, int) and vec_body == 0:
            vec_body = np.zeros((w2v_size,))

    try:
        cs = cosine_similarity(vec_head.reshape(1, -1), vec_body.reshape(1, -1))
    except:
        print(vec_head.reshape(1, -1).shape, vec_body.reshape(1, -1).shape)
        print(vec_head, "\n", vec_body)
        exit()
    return cs


def tokenize(data, stop_words=stop_words):
    token_pattern = re.compile(r"(?u)\b\w\w+\b", flags=re.UNICODE | re.LOCALE)
    splited_data = token_pattern.findall(data)
    splited_data = [x for x in splited_data if len(x) > 3]
    return splited_data

def get_w2v_feature_vector(head, body, bow_vec, tfreq_vec, tfidf_vec):
    test_set = []
    heads_track = {}
    bodies_track = {}
    cos_track = {}
    headlines = []
    body_ids = []
    # load our w2v model    
    w2v_model = joblib.load("/home/fndetect/server/pickle/w2v_model.pkl")
    head_bow = bow_vec.transform([head]).toarray()
    head_tf = tfreq_vec.transform(head_bow).toarray()[0].reshape(1,-1)

    body_bow = bow_vec.transform([body]).toarray()
    body_tf = tfreq_vec.transform(body_bow).toarray()[0].reshape(1,-1)

    head_tfidf = tfidf_vec.transform([head]).toarray().reshape(1,-1)
    body_tfidf = tfidf_vec.transform([body]).toarray().reshape(1,-1)

    tfidf_cos = cosine_similarity(head_tfidf, body_tfidf)[0].reshape(1,1)
    w2v_cs = get_w2v_cs(w2v_model, head, body)

    feat_vec = np.squeeze(np.c_[head_tf, body_tf, tfidf_cos, w2v_cs])
    return feat_vec.reshape(-1,1)
