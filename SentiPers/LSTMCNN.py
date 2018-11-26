# Now It's time to feed vectors into NN classifier
# Using Keras
from keras.models import Sequential
from SentiPers import WordEmbedding
from keras.layers import Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation
from keras.layers.embeddings import Embedding

print("x_train and y_train shape is : ", WordEmbedding.train_vecs_w2v.shape, WordEmbedding.y_train.shape)
print("x_test and y_test shape is : ", WordEmbedding.test_vesc_w2v.shape, WordEmbedding.y_test.shape)

model = Sequential()
# weights must be replaced with a matrix that store index of each words
# Check this out
# https://blog.keras.io/using-pre-trained-word-embeddings-in-a-keras-model.html
model.add(Embedding(input_dim=WordEmbedding.train_vecs_w2v.shape[0], output_dim=WordEmbedding.train_vecs_w2v.shape[1],
                    weights=[WordEmbedding.train_vecs_w2v], trainable=False,  input_length=200))
model.add(Dropout(0.2))
model.add(Conv1D(64, 5, activation='relu'))
model.add(MaxPooling1D(pool_size=4))
model.add(LSTM(200))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(WordEmbedding.train_vecs_w2v, WordEmbedding.y_train, validation_split=0.05, epochs=3)
score = model.evaluate(WordEmbedding.test_vesc_w2v, WordEmbedding.y_test)
print("Accuracy: ", score[1])
