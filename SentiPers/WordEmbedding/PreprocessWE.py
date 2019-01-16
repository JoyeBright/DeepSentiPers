import codecs
import os
from hazm import *
from SentiPers import Loader
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from SentiPers.Router import ROOT_DIR
from SentiPers import VocabularyMaker
from stopwords_guilannlp import stopwords_output

# Number of words used in Tokenizer
num_words = 2500

# Make vocabulary
VocabularyMaker.make_list()


# Load vocabulary
def load_doc(filename):
    file = codecs.open(filename, 'r', "utf8")
    text = file.read()
    file.close()
    return text


# load the vocabulary
vocab_filename = os.path.join(ROOT_DIR, 'outputs/vocab.txt')
vocab = load_doc(vocab_filename)
vocab = vocab.split()
vocab = set(vocab)
print('The size of vocab made by VocabularyMaker.py ', len(vocab))
x_train, x_test, y_train, y_test = Loader.get_data()

# Get stop words
stop_set = stopwords_output("Persian", "set")


# turn a doc into clean tokens
def clean_doc(doc, vocabulary):
    tokenized = word_tokenize(doc)  # Tokenize text
    tokens = [w for w in tokenized if not w in stop_set]    # Remove stop words
    tokens = [w for w in tokens if not len(w) <= 1]
    tokens = [w for w in tokens if not w.isdigit()]
    tokens = [w for w in tokens if w in vocabulary]
    tokens = ' '.join(tokens)
    return tokens


train_docs = list()
for document in x_train:
    train_docs.append(clean_doc(document, vocab))


# create the tokenizer
tokenizer = Tokenizer(num_words=num_words)
# fit the tokenizer on the documents
tokenizer.fit_on_texts(train_docs)
# sequence encode
encoded_docs = tokenizer.texts_to_sequences(train_docs)

# pad sequences
max_length = max([len(s.split()) for s in train_docs])
x_train_reshaped = pad_sequences(encoded_docs, maxlen=max_length, padding='post')

test_docs = list()
for document in x_test:
    test_docs.append(clean_doc(document, vocab))

encoded_docs = tokenizer.texts_to_sequences(test_docs)
x_test_reshaped = pad_sequences(encoded_docs, maxlen=max_length, padding='post')


# define vocabulary size (largest integer value)
vocab_size = len(tokenizer.word_index) + 1

# print("The size of vocab made by Keras tokenizer", vocab_size)
# print(x_train_reshaped.shape)
# print(x_test_reshaped.shape)


def get_data():
    return x_train_reshaped, x_test_reshaped, y_train, y_test


def get_sizes():
    return vocab_size, max_length
