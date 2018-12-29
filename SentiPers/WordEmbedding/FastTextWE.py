from SentiPers.Router import ROOT_DIR
import os
import numpy as np
from gensim.models import KeyedVectors
from SentiPers.WordEmbedding import PreprocessWE

EMBEDDING_FILE = os.path.join(ROOT_DIR, 'wiki.fa.vec')
embed_size = 300


# We can also use a gensim model called KeyedVectors
def gensim_model_based(file_address):
    # Creating the model
    en_model = KeyedVectors.load_word2vec_format(file_address)
    # Getting the tokens
    words = []
    for word in en_model.vocab:
        words.append(word)

    return en_model, words


model, words = gensim_model_based(EMBEDDING_FILE)

# We get the mean and standard deviation of the embedding weights so that we could maintain the
# same statistics for the rest of our own random generated weights.\
embedding_list = list()
for w in words:
    embedding_list.append(model[w])
all_embs = np.stack(embedding_list)
emb_mean, emb_std = all_embs.mean(), all_embs.std()
tokenizer = PreprocessWE.tokenizer
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

