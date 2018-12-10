from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC, SVC
from sklearn.pipeline import Pipeline
import os
import pandas as pd
from stopwords_guilannlp import stopwords_output
from hazm import *

# total number = 7415
n = 7415
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def ingest():
    CONFIG_PATH = os.path.join(ROOT_DIR.replace('Classifier', ''), 'data.csv')
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
x_train, x_test, y_train, y_test = train_test_split(ingest.head(n).Text,
                                                    ingest.head(n).Value)

# Make stopword set
stop_words = stopwords_output("Persian", "nar")
stop_list = []
for s in stop_words:
    stop_list.append(s[0])
stop_set = set(stop_list)


# Tokenize function used in Vectorizer
def tokenize(text):
    return word_tokenize(text)


# (Multinomial) Naive Bayes Model
text_clf = Pipeline([('vect', CountVectorizer(tokenizer=tokenize, stop_words=stop_set,
                                              analyzer='word', ngram_range=(1, 2), min_df=5)),
                     ('tfidf', TfidfTransformer(sublinear_tf=True)),
                     ('clf', MultinomialNB())])
text_clf = text_clf.fit(x_train, y_train)
naive_score = text_clf.score(x_test, y_test)
print('Naive Bayes Model: ', naive_score)
predict = text_clf.predict(x_test)

# SGD (Stochastic Gradient Descent) Model
text_clf_sgd = Pipeline([('vect', CountVectorizer(tokenizer=tokenize, stop_words=stop_set,
                                                  analyzer='word', ngram_range=(1, 2), min_df=5)),
                         ('tfidf', TfidfTransformer(sublinear_tf=True)),
                         ('clf-svm', SGDClassifier(loss='hinge', penalty='l2',
                                                   alpha=1e-3, max_iter=5))])
text_clf_sgd = text_clf_sgd.fit(x_train, y_train)
sgd_score = text_clf_sgd.score(x_test, y_test)
print('SGD Model: ', sgd_score)

# Linear Support Vector Machine Model
text_clf_linear_svc = Pipeline([('vect', CountVectorizer(tokenizer=tokenize, stop_words=stop_set,
                                                  analyzer='word', ngram_range=(1, 2), min_df=5)),
                         ('tfidf', TfidfTransformer(sublinear_tf=True)),
                         ('clf-svm', LinearSVC(loss='hinge', penalty='l2', max_iter=5))])
text_clf_linear_svc = text_clf_linear_svc.fit(x_train, y_train)
linear_svc_score = text_clf_linear_svc.score(x_test, y_test)
print('Linear SVC Model: ', linear_svc_score)


# Multi-class Support Vector Classification Model
text_clf_svc = Pipeline([('vect', CountVectorizer(tokenizer=tokenize, stop_words=stop_set,
                                                  analyzer='word', ngram_range=(1, 2), min_df=5)),
                         ('tfidf', TfidfTransformer(sublinear_tf=True)),
                         ('clf-svm', SVC(kernel='rbf'))])
text_clf_svc = text_clf_svc.fit(x_train, y_train)
svc_score = text_clf_svc.score(x_test, y_test)
print('Multi-class SVC Model: ', svc_score)
