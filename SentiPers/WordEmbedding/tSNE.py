from __future__ import print_function
from gensim.models import KeyedVectors
import numpy as np
from sklearn.manifold import TSNE
import plotly.offline as py
import plotly.graph_objs as go
import os
from SentiPers.Router import ROOT_DIR

EMBEDDING_FILE = os.path.join(ROOT_DIR, 'wiki.fa.vec')
# Loading the vectors
# [Warning] Takes a lot of time
en_model = KeyedVectors.load_word2vec_format(EMBEDDING_FILE)

# Limit number of tokens to be visualized
limit = 1000
vector_dim = 300

# Getting tokens and vectors
words = []
embedding = np.array([])
i = 0
for word in en_model.vocab:
    # Break the loop if limit exceeds
    if i == limit:
        break

    # Getting token
    words.append(word)

    # Appending the vectors
    embedding = np.append(embedding, en_model[word])

    i += 1

# Reshaping the embedding vector
embedding = embedding.reshape(limit, vector_dim)


# Creating the tsne plot [Warning: will take time]
tsne = TSNE(perplexity=30.0, n_components=2, init='pca', n_iter=5000)

low_dim_embedding = tsne.fit_transform(embedding)

# Finally plotting and saving the fig
plots = []
for i in range(len(words)):
    pl = go.Scatter(x=[low_dim_embedding[i, 0]], y=[low_dim_embedding[i, 1]], mode='markers+text', text=[words[i]],
                    textposition='bottom center', marker=dict(size=10, color=i, colorscale='Jet', opacity=0.8),
                    textfont=dict(size=14, ), name=words[i])
    plots.append(pl)

py.plot(plots, filename=os.path.join(ROOT_DIR, 'outputs/tsne.html'), auto_open=True)
