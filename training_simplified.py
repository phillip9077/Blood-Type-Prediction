import numpy as np
import pandas as pd
from keras import losses
from keras import optimizers
from tensorflow import keras

# loading the .csv file into the program
dataframe = pd.read_csv('C:/VIA Tech/Blood Type Prediction/Blood_types_simplified.csv',
                        ).values

X = []
y = []
blood_types = {'A': [1, 0, 0, 0],
               'B': [0, 1, 0, 0],
               'AB': [0, 0, 1, 0],
               'O': [0, 0, 0, 1]}

for row in dataframe:
    first_type = np.array(blood_types[row[0]])
    second_type = np.array(blood_types[row[1]])
    resultType = np.array(blood_types[row[2]])
    input_arr = first_type | second_type
    X.append(input_arr)
    y.append(resultType)

X = np.array(X)
y = np.array(y)

# setting up an ANN; can't use a Sequential model because there are two inputs
# input layer is 4 neurons (4 possible blood types for each parent, but concatenated into one array)
# output layer is 4 neurons (4 possible blood types for the next generation)
inputs = keras.Input(shape=(4,))
layer1 = keras.layers.Dense(512, activation='relu')(inputs)
layer2 = keras.layers.Dense(256, activation='relu')(layer1)
outputs = keras.layers.Dense(4, activation='softmax')(layer2)
model = keras.Model(inputs=inputs, outputs=outputs, name='bloodtype_model')
print(model.summary())

# training the model
model.compile(
    loss=losses.CategoricalCrossentropy(from_logits=True),
    optimizer=optimizers.Adam(),
    metrics=['accuracy'],
)

model.fit(X, y, batch_size=8, epochs=500, shuffle=True)

results = model.evaluate(X, y, verbose=0)
print('Loss = ', results[0])
print('Accuracy = ', results[1])

# model.save('C:/VIA Tech/Blood Type Prediction')

# Once the model is trained once, you can just uncomment the line below and comment out the
# model.fit and model.save line (Line 61 and 67).
# model = keras.models.load_model('C:/VIA Tech/Blood Type Prediction')

is_quit = False
while not is_quit:
    type_one = input("Type your first parent's blood type: ").capitalize()
    type_two = input("Type your second parent's blood type: ").capitalize()
    temp = np.array(blood_types[type_one]) | np.array(blood_types[type_two])
    temp = np.ndarray.tolist(temp)
    prediction = model.predict([temp])[0]
    print("The AI predicts the possibilities of your potential blood types are: ", prediction)
    end = input("Do you want to continue? ")
    if end == "No" or end == "no":
        is_quit = True
