from SentiPers.WordEmbedding import FastTextWE
from SentiPers.WordEmbedding import KerasWE
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.layers import Bidirectional, GlobalMaxPool1D,Bidirectional
from keras.models import Model
from keras.utils.np_utils import to_categorical
from keras.metrics import categorical_accuracy

maxlen = KerasWE.max_length
tokenizer = KerasWE.tokenizer
x_train, x_test, y_train, y_test = KerasWE.get_data()
embedding_matrix = FastTextWE.embedding_matrix

categorical_y_train = to_categorical(y_train, 5)
categorical_y_test = to_categorical(y_test, 5)

inp = Input(shape=(maxlen, ))
x = Embedding(len(tokenizer.word_index), embedding_matrix.shape[1], weights=[embedding_matrix], trainable=False)(inp)
x = Bidirectional(LSTM(60, return_sequences=True, name='lstm_layer', dropout=0.1, recurrent_dropout=0.1))(x)
x = GlobalMaxPool1D()(x)
x = Dropout(0.1)(x)
x = Dense(50, activation="relu")(x)
x = Dropout(0.1)(x)
x = Dense(5, activation="sigmoid")(x)

model = Model(inputs=inp, outputs=x)
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=[categorical_accuracy])

model.summary()

batch_size = 32
epochs = 4
hist = model.fit(x_train, categorical_y_train, batch_size=batch_size, epochs=epochs)

loss, acc = model.evaluate(x_test, categorical_y_test, verbose=0)
print('Test Accuracy: %f' % (acc*100))
