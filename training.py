import numpy as np
import pandas as pd
from keras import losses
from keras import optimizers
from tensorflow import keras

# reading blood type data
dataframe = pd.read_csv('C:/VIA Tech/Blood Type Prediction/Blood types.csv',
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


def mergeList(firstType, secondType):
    inputArr = []
    for i in range(len(firstType)):
        if firstType[i] != secondType[i]:
            if firstType[i] == 1:
                inputArr.append(firstType[i])
            elif secondType[i] == 1:
                inputArr.append(secondType[i])
        else:
            inputArr.append(firstType[i])
    return inputArr


# inputs and outputs both are one-hot encoded
for row in dataframe:
    first_type = blood_types[row[0]]
    second_type = blood_types[row[1]]
    resultType = blood_types[row[2]]
    input_arr = mergeList(first_type, second_type)
    X.append(input_arr)
    y.append(resultType)

X = np.array(X)
y = np.array(y)

# X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

# setting up an ANN; can't use a Sequential model because there are two inputs
# input layer is 16 neurons (8 possible blood types for each parent)
# output layer is 8 neurons (8 possible blood types for the next generation)
inputs = keras.Input(shape=(8,))
layer1 = keras.layers.Dense(1024, activation='relu')(inputs)
layer2 = keras.layers.Dense(512, activation='relu')(layer1)
outputs = keras.layers.Dense(8, activation='softmax')(layer2)
model = keras.Model(inputs=inputs, outputs=outputs, name='bloodtype_model')
print(model.summary())

# training the model
model.compile(
    loss=losses.CategoricalCrossentropy(from_logits=True),
    optimizer=optimizers.Adam(),
    metrics=['accuracy'],
)

model.fit(X, y, batch_size=32, epochs=500, shuffle=True)

results = model.evaluate(X, y, verbose=0)
print('Loss = ', results[0])
print('Accuracy = ', results[1])

model.save('C:/VIA Tech/Blood Type Prediction')

# Once the model is trained once, you can just uncomment the line below and comment out the
# model.fit and model.save line (Line 58 and 70).
# model = keras.models.load_model('C:/VIA Tech/Blood Type Prediction')

is_quit = False
while not is_quit:
    type_one = input("Type your first parent's blood type: ")
    type_two = input("Type your second parent's blood type: ")
    type_one_plus = type_one + "+"
    type_two_plus = type_two + "+"
    type_one_minus = type_one + "-"
    type_two_minus = type_two + "-"
    prediction_plus = model.predict([mergeList(blood_types[type_one_plus],
                                               blood_types[type_two_plus])])[0]
    prediction_minus = model.predict([mergeList(blood_types[type_one_minus],
                                                blood_types[type_two_minus])])[0]
    prediction = []
    for i, val in np.ndenumerate(prediction_plus):
        prediction.append((val + prediction_minus[i]) / 2)
    print("The AI predicts the possibilities of your potential blood types are: ", prediction)
    end = input("Do you want to continue? ")
    if end == "No" or end == "no":
        is_quit = True
