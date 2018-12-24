from collections import Counter
from hazm import *
import codecs
from SentiPers import Loader, StopWords

# Get data
x_train, x_test, y_train, y_test = Loader.get_data()

# Get stop words
stop_set = StopWords.get_stop_set()


def add_to_vocab(text):
    tokenized = tokenize(text)  # Tokenize text
    tokens = [w for w in tokenized if not w in stop_set]    # Remove stop words
    tokens = [w for w in tokens if not len(w) <= 1]
    tokens = [w for w in tokens if not w.isdigit()]
    vocab.update(tokens)    # Add tokens to vocabulary


def tokenize(text):
    return word_tokenize(text)


vocab = Counter()   # Make vocabulary
for text in x_train:
    add_to_vocab(text)

# print the size of the vocab
print(len(vocab))
# print the top words in the vocab
print(vocab.most_common(100))

min_occurance = 5
tokens = [k for k, c in vocab.items() if c >= min_occurance]
print(len(tokens))


# save list to file
def save_list(lines, filename):
    data = '\n'.join(lines)
    file = codecs.open(filename, 'w', "utf-8")
    file.write(data)
    file.close()


save_list(tokens, 'Outputs/vocab.txt')
