# Now It's time to feed vectors into NN classifier
# Using Keras
from keras.models import Sequential
from keras.layers import Dense
from SentiPers import WordEmbedding
from keras.layers import LSTM
from keras.layers import Activation

print("x_train and y_train shape is : ", WordEmbedding.train_vecs_w2v.shape, WordEmbedding.y_train.shape)
print("x_test and y_test shape is : ", WordEmbedding.test_vesc_w2v.shape, WordEmbedding.y_test.shape)

x_train = WordEmbedding.train_vecs_w2v.reshape((2400, 200, 1))
y_train = WordEmbedding.y_train.reshape((2400, 1))

x_test = WordEmbedding.test_vesc_w2v.reshape((600, 200, 1))
y_test = WordEmbedding.y_test.reshape((600, 1))

print("After reshape -> x_train and y_train shape is : ", x_train.shape, y_train.shape)
print("After reshape -> x_test and y_test shape is : ", x_test.shape, y_test.shape)


model = Sequential()
model.add(LSTM(8, input_shape=(200, 1), return_sequences=False))#True = many to many
model.add(Dense(2, kernel_initializer='normal', activation='linear'))
model.add(Dense(1, kernel_initializer='normal', activation='linear'))

model.compile(optimizer='rmsprop',
              loss='mse',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=2000, batch_size=5, verbose=2, validation_split=0.05)
score = model.evaluate(x_test, y_test)
print("Accurracy: ", score[1])
