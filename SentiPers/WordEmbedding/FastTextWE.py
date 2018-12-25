from SentiPers.Router import ROOT_DIR
import os
import codecs
from tqdm import tqdm
import numpy as np
from gensim.models import KeyedVectors
from SentiPers.WordEmbedding import KerasWE

EMBEDDING_FILE = os.path.join(ROOT_DIR, 'wiki.fa.vec')
embed_size = 300


def get_fasttext(file_address):
    # Make a global dictionary based on fasttext embedding
    embeddings_index = dict()
    f = codecs.open(file_address, 'r', "utf8")
    header_line = next(f)   # Skip header
    for line in tqdm(f):
        # split up line into an indexed array
        values = line.split()
        # first index is word
        word = values[0]
        try:
            # store the rest of the values in the array as a new array
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs  # 50 dimensions
        except ValueError:  # To ignore some
            print(word, "could not convert to float")
    f.close()
    print('Loaded %s word vectors.' % len(embeddings_index))
    # print(embeddings_index.get('گوشی'))

    return embeddings_index


# We can also use a gensim model called KeyedVectors
def gensim_model_based(file_address):
    # Creating the model
    en_model = KeyedVectors.load_word2vec_format(file_address)

    # Getting the tokens
    words = []
    for word in en_model.vocab:
        words.append(word)

    return en_model, words


def test_gensim_model(en_model, words):
    # Printing out number of tokens available
    print("Number of Tokens: {}".format(len(words)))

    # Printing out the dimension of a word vector
    print("Dimension of a word vector: {}".format(
        len(en_model[words[0]])
    ))

    # Print out the vector of a word
    print("Vector components of a word: {}".format(
        en_model[words[0]]
    ))

    # Pick a word
    find_similar_to = ['گوشی', 'موبایل', 'عالی', 'رشت']

    # Finding out similar words [default= top 10]
    for word in find_similar_to:
        for similar_word in en_model.similar_by_word(word):
            print("Word: {0}, Similarity: {1:.2f}".format(
                similar_word[0], similar_word[1]
            ))


# embeddings_index = get_fasttext(EMBEDDING_FILE)
model, words = gensim_model_based(EMBEDDING_FILE)
# test_gensim_model(model, words)

# We get the mean and standard deviation of the embedding weights so that we could maintain the
# same statistics for the rest of our own random generated weights.\
embedding_list = list()
for w in words:
    embedding_list.append(model[w])
all_embs = np.stack(embedding_list)
emb_mean, emb_std = all_embs.mean(), all_embs.std()
tokenizer = KerasWE.tokenizer
# We are going to set the embedding size to the pretrained dimension as we are replicating it
nb_words = len(tokenizer.word_index)
# the size will be Number of Words in Vocab X Embedding Size
embedding_matrix = np.random.normal(emb_mean, emb_std, (nb_words, embed_size))
# With the newly created embedding matrix, we'll fill it up with the words that we have in both
# our own dictionary and loaded pretrained embedding.
embeddedCount = 0
for word, i in tokenizer.word_index.items():
    i -= 1
    # then we see if this word is in glove's dictionary, if yes, get the corresponding weights
    if word in model.vocab:
        embedding_vector = model[word]
        # and store inside the embedding matrix that we will train later on.
        embedding_matrix[i] = embedding_vector
        embeddedCount += 1
    else:   # Unknown words
        embedding_vector = model['subdivision_name']
        # and store inside the embedding matrix that we will train later on.
        embedding_matrix[i] = embedding_vector
        embeddedCount += 1

print('total embedded:', embeddedCount, 'common words')
print('Embedding matrix shape:', embedding_matrix.shape)

