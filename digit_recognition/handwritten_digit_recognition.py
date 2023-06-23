from os.path import isfile

from cv2 import imread
from keras.datasets import mnist
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.utils import normalize
from numpy import invert, array, argmax

MODEL_TARGET_FILENAME: str = "handwritten_digit_recognition"
TRAINING_EPOCHS: int = 4  # careful not to overfit

if __name__ == '__main__':
    (data, d_label), (test, t_label) = mnist.load_data()

    data = normalize(data, axis=1)
    test = normalize(test, axis=1)

    model = Sequential()
    model.add(Flatten(input_shape=(28, 28)))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(data, d_label, epochs=TRAINING_EPOCHS)

    model.save(MODEL_TARGET_FILENAME)

    print()
    print(f'Training finished, model has been saved to {MODEL_TARGET_FILENAME}')
    print()

    digit: int
    for digit in range(1, 10):
        image_path: str = f'resources/hand{digit}.png'
        if isfile(image_path):
            try:
                img = imread(image_path)[:, :, 0]
                img = invert(array([img]))

                prediction = model.predict(img)
                print(f'Actual digit - {digit} | Prediction: {argmax(prediction)}')
            except Exception as e:
                print(e)
