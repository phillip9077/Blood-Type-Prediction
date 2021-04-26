import pandas as pd
import numpy as np
from sklearn import model_selection
from tensorflow import keras
from keras import losses
from keras import optimizers

# reading blood type data
dataframe = pd.read_csv('*wherever you put this project folder*/Blood types.csv',
                        ).values

X = []
y = []

# creating and splitting the dataset into training and testing datasets
blood_types = {'A+': [1, 0, 0, 0, 0, 0, 0, 0],
                'A-': [0, 1, 0, 0, 0, 0, 0, 0],
                'B+': [0, 0, 1, 0, 0, 0, 0, 0],
                'B-': [0, 0, 0, 1, 0, 0, 0, 0],
                'AB+': [0, 0, 0, 0, 1, 0, 0, 0],
                'AB-': [0, 0, 0, 0, 0, 1, 0, 0],
                'O+': [0, 0, 0, 0, 0, 0, 1, 0],
                'O-': [0, 0, 0, 0, 0, 0, 0, 1]}

for row in dataframe:
    # inputs and outputs both are one-hot encoded
    firstType = blood_types[row[0]]
    secondType = blood_types[row[1]]
    resultType = blood_types[row[2]]
    input_arr = firstType + secondType
    X.append(input_arr)
    y.append(resultType)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

# setting up an ANN; can't use a Sequential model because there are two inputs
# input layer is 16 neurons (8 possible blood types for each parent)
# output layer is 8 neurons (8 possible blood types for the next generation)
# inputs = keras.Input(shape=(16,))
# layer1 = keras.layers.Dense(32, activation='relu')(inputs)
# layer2 = keras.layers.Dense(16, activation='relu')(layer1)
# outputs = keras.layers.Dense(8, activation='softmax')(layer2)
# model = keras.Model(inputs=inputs, outputs=outputs, name='bloodtype_model')
# print(model.summary())
#
# # creating a learning rate schedule
# initial_learning_rate = 0.01
# lr_schedule = keras.optimizers.schedules.ExponentialDecay(
#     initial_learning_rate,
#     decay_steps=100000,
#     decay_rate=0.96,
#     staircase=True)
#
# # training the model
# model.compile(
#     loss=losses.CategoricalCrossentropy(from_logits=True),
#     optimizer=optimizers.SGD(learning_rate=lr_schedule),
#     metrics=['accuracy'],
# )
#
# model.fit(X_train, y_train, batch_size=23, epochs=500, validation_split=0.1, shuffle=True)
#
# results = model.evaluate(X_test, y_test, verbose=0)
# print('Loss = ', results[0])
# print('Accuracy = ', results[1])
#
# model.save('C:/VIA Tech/Blood Type Prediction')

model = keras.models.load_model('*wherever you put this project folder*/Blood Type Prediction')

is_quit = False
while not is_quit:
    type_one = input("Type your first parent's blood type: ")
    type_two = input("Type your second parent's blood type: ")
    type_one_plus = type_one + "+"
    type_two_plus = type_two + "+"
    type_one_minus = type_one + "-"
    type_two_minus = type_two + "-"
    prediction_plus = model.predict([blood_types[type_one_plus] + blood_types[type_two_plus]])[0]
    prediction_minus = model.predict([blood_types[type_one_minus] + blood_types[type_two_minus]])[0]
    prediction = []
    for i, val in np.ndenumerate(prediction_plus):
        prediction.append((val + prediction_minus[i]) / 2)
    print("The AI predicts the possibilities of your potential blood types are: ", prediction)
    end = input("Do you want to continue? ")
    if end == "No" or end == "no":
        is_quit = True


