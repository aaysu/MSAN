from keras.layers import Dropout
from keras.utils import np_utils
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense

(X_train, Y_train), (X_test, Y_test) = mnist.load_data()

# flatten 28*28 images to a 784 vector for each image
num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('float32')
X_test = X_test.reshape(X_test.shape[0], num_pixels).astype('float32')

# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255

# one hot encode outputs
Y_train = np_utils.to_categorical(Y_train)
Y_test = np_utils.to_categorical(Y_test)
num_classes = Y_test.shape[1]

def get_my_model(lr=0.001, M1=300, M2=100, w1=0.2, w2=0.2):
    model = Sequential()
    model.add(Dense(M1, input_dim=num_pixels, init='normal', activation='relu'))
    model.add(Dropout(w1))
    model.add(Dense(M2, activation='relu'))
    model.add(Dropout(w2))
    model.add(Dense(10, activation='softmax'))
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.optimizer.lr.set_value(lr)
    return model

model = get_my_model()
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), nb_epoch=30, batch_size=200, verbose=2)
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Testing Accuracy: %.2f%%" % (scores[1]*100))
scores2 = model.evaluate(X_train, Y_train, verbose=0)
print("Training Accuracy: %.2f%%" % (scores2[1]*100))
