# Now It's time to feed vectors into NN classifier
# Using Keras
from keras.models import Sequential
from keras.layers import Dense
from SentiPers.WordEmbedding import CustomizedWE
from keras.utils.np_utils import to_categorical
from keras.utils import plot_model


# Corpus has categorical value as its output so making categorical output is necessary
categorical_y_train = to_categorical(CustomizedWE.y_train, 5)
categorical_y_test = to_categorical(CustomizedWE.y_test, 5)

model = Sequential()
model.add(Dense(200, activation='relu', input_dim=CustomizedWE.n_dim))
model.add(Dense(150, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(5, activation='sigmoid'))
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print('Train ...')
model.fit(CustomizedWE.train_vecs_w2v, categorical_y_train,
          validation_data=(CustomizedWE.test_vesc_w2v, categorical_y_test),
          epochs=15, batch_size=32, verbose=2)
score = model.evaluate(CustomizedWE.test_vesc_w2v, categorical_y_test)
plot_model(model, show_shapes=True, to_file=CustomizedWE.ROOT_DIR + '/Outputs/CustomizedNN-CustomizedEmb.png')
print(score[1])
