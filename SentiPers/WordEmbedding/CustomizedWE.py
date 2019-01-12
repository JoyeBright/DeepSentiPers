import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from hazm import *
from tqdm import tqdm
import gensim
# https://pypi.org/project/stopwords-guilannlp/
from stopwords_guilannlp import stopwords_output
from gensim.models.word2vec import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import scale
from SentiPers.Router import ROOT_DIR
tqdm.pandas(desc="progress-bar")
pd.options.mode.chained_assignment = None
LabeledSentence = gensim.models.doc2vec.LabeledSentence

# Number of rows in data.csv
n = 7415
# Dimensionality of the word vectors
n_dim = 100


def ingest():
    CONFIG_PATH = os.path.join(ROOT_DIR, 'data.csv')
    data = pd.read_csv(CONFIG_PATH, sep='\t')
    data.drop(['Negative-Keywords', 'Neutral-Keywords', 'Positive-Keywords', 'Targets'], axis=1, inplace=True)
    data = data[data.Value.isnull() == False]
    # map applies a function on each cell of Value then if it null, it will set it with 0s
    data['Value'] = data['Value'].map(int)
    data = data[data['Text'].isnull() == False]
    data.reset_index(inplace=True)
    data.drop('index', axis=1, inplace=True)
    print('Dataset Loaded with shape', data.shape)
    return data


ingest = ingest()
# print(ingest['Text'].iloc[0])


# Persian Tokenizer: Hazm
# noinspection PyBroadException
def tokenize(s):
    try:
        tokens = word_tokenize(s)
        filtered_tokens = []
        stopwords = stopwords_output("Persian", "nar")
        for w in tokens:
            if w not in stopwords:
                filtered_tokens.append(w)
        return filtered_tokens
    except:
        return 'NC'


def postprocess(data):
    data['Tokens'] = data['Text']
    data = data.head(n)
    for i in range(0, n):
        token = tokenize(data['Text'].iloc[i])
        data['Tokens'].iloc[i] = token
    data = data[data.Tokens != 'NC']
    data.reset_index(inplace=True)
    data.drop('index', inplace=True, axis=1)
    # Monitor the final structure of data
    CONFIG_PATH = os.path.join(ROOT_DIR, 'Outputs/postprocess_data.csv')
    data.to_csv(CONFIG_PATH, sep="\t")
    print("\nAfter Postprocessing, shape of data is equal:", data.shape)
    return data


postprocess = postprocess(ingest)
# print(d['Tokens'].iloc[0])
# print(postprocess.head())

# Define Training and Test set
x_train, x_test, y_train, y_test = train_test_split(postprocess.head(n).Tokens,
                                                    postprocess.head(n).Value)
print("Shape of x_train ", x_train.shape)
print("Shape of y_train ", y_train.shape)
# We'd like to save the X_train and X_test
x_train_csv = x_train.to_frame()
x_test_csv = x_test.to_frame()
CONFIG_PATH1 = os.path.join(ROOT_DIR, 'Outputs/x_train.csv')
CONFIG_PATH2 = os.path.join(ROOT_DIR, 'Outputs/x_test.csv')
x_train_csv.to_csv(CONFIG_PATH1, sep="\t")
x_test_csv.to_csv(CONFIG_PATH2, sep="\t")


def labelizeSent(data, label_type):
    labelized = []
    for i, v in tqdm(enumerate(data)):
        label = '%s_%s' % (label_type, i)
        labelized.append(LabeledSentence(v, [label]))
    return labelized


x_train = labelizeSent(x_train, 'TRAIN')
x_test = labelizeSent(x_test, 'TEST')

# print(x_train[0].words)
# print(x_train[0])
# Build Word2Vec Model from x-train
sentipers_w2v = Word2Vec(size=n_dim, min_count=10, window=5)
sentipers_w2v.build_vocab([x.words for x in tqdm(x_train)])
sentipers_w2v.train([x.words for x in tqdm(x_train)], total_examples=n, epochs=5)
sentipers_w2v.wv.save_word2vec_format(fname=ROOT_DIR+"/Outputs/vectors.txt", fvocab=None, binary=False)

np.set_printoptions(threshold=np.nan)
# print(sentipers_w2v.wv.vocab)
# print(sentipers_w2v['فکس'])
# Word2Vec has a great feature which provides a cool method named most_similar, this method
# returns the top n similar ones.
# print(sentipers_w2v.most_similar('فکس'))
# print(sentipers_w2v.most_similar('گوشی'))


print("Building tf-idf matrix ...")
# TfidfVectorizer convert a collection of raw documents to a matrix of TF-IDF features
# min_df ignore terms that have a document frequency strictly higher than the given threshold
vectorizer = TfidfVectorizer(analyzer=lambda x: x, min_df=6)
# fit_transform learn vocabulary and idf, return term-document matrix
matrix = vectorizer.fit_transform([x.words for x in x_train])
# get_feature_names Array mapping from feature integer indices to feature name
tfidf = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))
print("Vocabulary size: ", len(tfidf))
# print(matrix)
# print(tfidf)


# The following function, create an averaged sentipers vector (from tokens)
def buildWordVector(tokens, size):
    vec = np.zeros(size).reshape((1, size))
    count = 0
    for word in tokens:
        try:
            vec += sentipers_w2v[word].reshape((1, size)) * tfidf[word]
            count += 1
        except KeyError:

            continue
    if count != 0:
        vec /= count
    return vec


# now convert x_train and x_test into list of vectors using the top function
train_vecs_w2v = np.concatenate([buildWordVector(z, n_dim) for z in
                                 tqdm(map(lambda x: x.words, x_train))])


# Standardize a dataset along any axis
train_vecs_w2v = scale(train_vecs_w2v)

test_vesc_w2v = np.concatenate([buildWordVector(z, n_dim) for z in
                                tqdm(map(lambda x: x.words, x_test))])
test_vesc_w2v = scale(test_vesc_w2v)

# print(train_vecs_w2v)
# print(test_vecs_w2v)
