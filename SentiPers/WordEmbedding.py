import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from hazm import *
from tqdm import tqdm
import gensim
from gensim.models.word2vec import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import scale
tqdm.pandas(desc="progress-bar")
pd.options.mode.chained_assignment = None
LabeledSentence = gensim.models.doc2vec.LabeledSentence


n = 3000
n_dim = 200


def ingest():
    data = pd.read_csv('Data.csv', sep='\t')
    data.drop(['Negative-Keywords', 'Neutral-Keywords', 'Positive-Keywords', 'Targets'], axis=1, inplace=True)
    data = data[data.Value.isnull() == False]
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
        return tokens
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
    return data


postprocess = postprocess(ingest)
# print(d['Tokens'].iloc[0])
# print(postprocess.head())

# Define Training and Test set
x_train, x_test, y_train, y_test = train_test_split(np.array(postprocess.head(n).Tokens),
                                                    np.array(postprocess.head(n).Value),
                                                    test_size=0.2)


def labelizeSent(data, label_type):
    labelized = []
    for i, v in tqdm(enumerate(data)):
        label = '%s_%s' % (label_type, i)
        labelized.append(LabeledSentence(v, [label]))
    return labelized


x_train = labelizeSent(x_train, 'TRAIN')
x_test = labelizeSent(x_test, 'TEST')

# print(x_train[0])
# Build Word2Vec Model from x-train
sentipers_w2v = Word2Vec(size=n_dim, min_count=10)
sentipers_w2v.build_vocab([x.words for x in tqdm(x_train)])
sentipers_w2v.train([x.words for x in tqdm(x_train)], total_examples=1, epochs=1)


# print(sentipers_w2v['خوب'])
# Word2Vec has a great feature which provides a cool method named most_similar, this method
# returns the top n similar ones.
# print(sentipers_w2v.most_similar('خوب'))
# print(sentipers_w2v.most_similar('عالی'))


print("Building tf-idf matrix ...")
# TfidfVectorizer convert a collection of raw documents to a matrix of TF-IDF features
# min_df ignore terms that have a document frequency strictly higher than the given threshold
vectorizer = TfidfVectorizer(analyzer=lambda x: x, min_df=10)
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
