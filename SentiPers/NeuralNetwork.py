# Now It's time to feed vectors into NN classifier
# Using Keras
from keras.models import Sequential
from keras.layers import Dense
from SentiPers import WordEmbedding


model = Sequential()
model.add(Dense(32, activation='relu', input_dim=WordEmbedding.n_dim))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(WordEmbedding.train_vecs_w2v, WordEmbedding.y_train, epochs=9, batch_size=32, verbose=2)
score = model.evaluate(WordEmbedding.test_vesc_w2v, WordEmbedding.y_test)
print(score[1])
