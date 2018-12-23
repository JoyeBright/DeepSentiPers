# Now It's time to feed vectors into NN classifier
# Using Keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, SpatialDropout1D
from SentiPers.WordEmbedding import CustomizedWE
from keras.utils.np_utils import to_categorical
from keras.utils import plot_model
from keras.metrics import categorical_accuracy

print("Shape of X_Train:", CustomizedWE.train_vecs_w2v.shape)
print("Shape of X_Test:", CustomizedWE.test_vesc_w2v.shape)
# print(WordEmbedding.train_vecs_w2v[0])
categorical_y_train = to_categorical(CustomizedWE.y_train, 5)
categorical_y_test = to_categorical(CustomizedWE.y_test, 5)
# print(categorical_y_train[0])

dropout_probability = 0.25
num_features = CustomizedWE.train_vecs_w2v.shape

# The input to every LSTM layer must be three dimensional.
# Samples. One sample is one sequence.
# Time Steps
# Features
x_train = CustomizedWE.train_vecs_w2v.reshape((5561, 100, 1))
x_test = CustomizedWE.test_vesc_w2v.reshape((1854, 100, 1))

# input_shape(time steps, features)
model = Sequential()
model.add(LSTM(100, return_sequences=True, activation="sigmoid",
               input_shape=(100, 1)))
print("Layer0 input shape:", model.layers[0].input_shape)
print("Layer0 output shape:", model.layers[0].output_shape)

model.add(LSTM(100, return_sequences=True, activation="sigmoid",
               input_shape=(100, 1)))
print("Layer1 input shape:", model.layers[1].input_shape)
print("Layer1 output shape:", model.layers[1].output_shape)

model.add(SpatialDropout1D(dropout_probability))

model.add(LSTM(100, return_sequences=False, activation="sigmoid"))
print("Layer2 input shape:", model.layers[2].input_shape)
print("Layer2 output shape:", model.layers[2].output_shape)

model.add(Dense(100, activation='softmax'))
print("Layer3 input shape:", model.layers[3].input_shape)
print("Layer3 output shape:", model.layers[3].output_shape)

model.add(Dense(5, activation="softmax"))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=[categorical_accuracy])

print(model.summary())
print("Training ....")
model.fit(x_train, categorical_y_train,
          validation_data=(x_test, categorical_y_test),
          batch_size=64, epochs=2, verbose=2)
score = model.evaluate(x_test, categorical_y_test)
plot_model(model, show_shapes=True, to_file=CustomizedWE.ROOT_DIR + '/Outputs/LSTM-Model.png')

print("Accuracy: ", score[1])



