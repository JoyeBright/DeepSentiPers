from collections import Counter
from hazm import *
import codecs
from SentiPers import Loader, StopWords
import os
from SentiPers.Router import ROOT_DIR

# Get data
x_train, x_test, y_train, y_test = Loader.get_data()

# Get stop words
stop_set = StopWords.get_stop_set()


def add_to_vocab(t):
    tokenized = tokenize(t)  # Tokenize text
    tokenized_temp = [w for w in tokenized if not w in stop_set]    # Remove stop words
    tokenized_temp = [w for w in tokenized_temp if not len(w) <= 1]
    tokenized_temp = [w for w in tokenized_temp if not w.isdigit()]
    vocab.update(tokenized_temp)    # Add tokens to vocabulary


def tokenize(t):
    return word_tokenize(t)


vocab = Counter()   # Make vocabulary
for text in x_train:
    add_to_vocab(text)

# print the size of the vocab
# print(len(vocab))
# print the top words in the vocab
# print(vocab.most_common(100))

min_occurrence = 4
tokens = [k for k, c in vocab.items() if c >= min_occurrence]
# print(len(tokens))


# save list to file
def save_list(lines, filename):
    data = '\n'.join(lines)
    file = codecs.open(filename, 'w', "utf-8")
    file.write(data)
    file.close()


def make_list():
    save_list(tokens, os.path.join(ROOT_DIR, 'outputs/vocab.txt'))
