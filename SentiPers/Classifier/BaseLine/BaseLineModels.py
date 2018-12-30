from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC, SVC
from sklearn.pipeline import Pipeline
from hazm import *
from SentiPers import Loader
from stopwords_guilannlp import stopwords_output

x_train, x_test, y_train, y_test = Loader.get_data()

# Make stop word set
stop_set = stopwords_output("Persian", "set")

# When building the vocabulary ignore terms that have a document frequency strictly lower than
# the given threshold. This value is also called cut-off in the literature.
min_df = 5


# Tokenize function used in Vectorizer
def tokenize(text):
    return word_tokenize(text)


# (Multinomial) Naive Bayes Model
text_clf = Pipeline([('vect', CountVectorizer(tokenizer=tokenize,
                                              analyzer='word', ngram_range=(1, 2), min_df=min_df, lowercase=False)),
                     ('tfidf', TfidfTransformer(sublinear_tf=True)),
                     ('clf', MultinomialNB())])
text_clf = text_clf.fit(x_train, y_train)
naive_score = text_clf.score(x_test, y_test)
print('Naive Bayes Model: ', naive_score)
predict = text_clf.predict(x_test)

# SGD (Stochastic Gradient Descent) Model
text_clf_sgd = Pipeline([('vect', CountVectorizer(tokenizer=tokenize,
                                                  analyzer='word', ngram_range=(1, 2), min_df=min_df, lowercase=False)),
                         ('tfidf', TfidfTransformer(sublinear_tf=True)),
                         ('clf-svm', SGDClassifier(loss='hinge', penalty='l2',
                                                   alpha=1e-3, max_iter=5))])
text_clf_sgd = text_clf_sgd.fit(x_train, y_train)
sgd_score = text_clf_sgd.score(x_test, y_test)
print('SGD Model: ', sgd_score)

# Linear Support Vector Machine Model
text_clf_linear_svc = Pipeline([('vect', CountVectorizer(tokenizer=tokenize,
                                                         analyzer='word', ngram_range=(1, 2),
                                                         min_df=min_df, lowercase=False)),
                                ('tfidf', TfidfTransformer(sublinear_tf=True)),
                                ('clf-svm', LinearSVC(loss='hinge', penalty='l2',
                                                      max_iter=5))])

text_clf_linear_svc = text_clf_linear_svc.fit(x_train, y_train)
linear_svc_score = text_clf_linear_svc.score(x_test, y_test)
print('Linear SVC Model: ', linear_svc_score)


# Multi-class Support Vector Classification Model
text_clf_svc = Pipeline([('vect', CountVectorizer(tokenizer=tokenize,
                                                  analyzer='word', ngram_range=(1, 2), min_df=min_df, lowercase=False)),
                         ('tfidf', TfidfTransformer(sublinear_tf=True)),
                         ('clf-svm', SVC(kernel='rbf'))])
text_clf_svc = text_clf_svc.fit(x_train, y_train)
svc_score = text_clf_svc.score(x_test, y_test)
print('Multi-class SVC Model: ', svc_score)
