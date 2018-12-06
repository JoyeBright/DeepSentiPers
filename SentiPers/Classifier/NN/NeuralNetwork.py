# Now It's time to feed vectors into NN classifier
# Using Keras
from keras.models import Sequential
from keras.layers import Dense
from SentiPers import WordEmbedding
from keras.utils.np_utils import to_categorical


# Corpus has categorical value as its output so making categorical output is necessary
categorical_y_train = to_categorical(WordEmbedding.y_train, 5)
categorical_y_test = to_categorical(WordEmbedding.y_test, 5)

model = Sequential()
model.add(Dense(200, activation='relu', input_dim=WordEmbedding.n_dim))
model.add(Dense(150, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(5, activation='sigmoid'))
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(WordEmbedding.train_vecs_w2v, categorical_y_train, epochs=10, batch_size=32, verbose=2)
score = model.evaluate(WordEmbedding.test_vesc_w2v, categorical_y_test)
print(score[1])
