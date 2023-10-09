import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models

df = pd.read_csv("outputCpy.csv")


import keras.backend as K

def get_f1(y_true, y_pred): #taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val


print(df.columns)

X = df.drop(columns=['Unnamed: 0','file_id','start_date','end_date','location','text','enrollment','Enrollment_rate','bioBert_values'], axis=1)
Y = df['Enrollment_rate']

X_train, X_test, Y_train, Y_test = X[:2500], X[2500:], Y[:2500], Y[2500:]



model = models.Sequential()



# Add a Convolutional layer

model.add(layers.Conv1D(64, kernel_size=3, activation='relu', input_shape=(769, 1)))

model.add(layers.MaxPooling1D(pool_size=2))

model.add(layers.Flatten())

# Add a fully connected (Dense) layer
model.add(layers.Dense(128, activation='relu'))

# Add the output layer
model.add(layers.Dense(10, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['accuracy'])

# Display the model summary
model.summary()

accuracy = model.evaluate(X_test, Y_test)

# model = keras.Sequential([
#                           keras.layers.Flatten(input_shape=(769,)),
#                           keras.layers.Dense(512, activation='relu'),
#                           keras.layers.Dense(128, activation='relu'),
#                           keras.layers.Dense(32, activation='relu'),
#                           keras.layers.Dense(8, activation='relu'),
#                           keras.layers.Dense(1, activation='sigmoid')
# ])

# # Compiling The Neural Network
# model.compile(optimizer='adam',
#               loss='mean_squared_error',
#               metrics=['accuracy',get_f1])

# # We choose sparse_categorical_crossentropy because number of labels are less

# # Training The Neural Network
# history = model.fit(X_train, Y_train, validation_split=0.1, epochs=20)

# # Visualizing accuracy and loss
# plt.plot(history.history['accuracy'])
# plt.plot(history.history['val_accuracy'])

# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')

# plt.legend(['training data', 'validation data'], loc = 'lower right')

# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])

# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')

# plt.legend(['training data', 'validation data'], loc = 'upper right')

# # loss, accuracy = model.evaluate(X_test, Y_test)
# # print(accuracy)

# Y_pred = model.predict(X_test)
# # test_output = model.predict(x_test, verbose=1)


# # Converting prediction probability to  labels
# Y_pred_labels = [np.argmax(i) for i in Y_pred]
# print(Y_pred_labels)

