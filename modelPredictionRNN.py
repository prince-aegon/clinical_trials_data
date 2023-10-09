import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models


df = pd.read_csv("outputCpy.csv")

X = df.drop(columns=['Unnamed: 0','file_id','start_date','end_date','location','text','enrollment','Enrollment_rate','bioBert_values'], axis=1)
Y = df['Enrollment_rate']

X_train, X_test, Y_train, Y_test = X[:2500], X[2500:], Y[:2500], Y[2500:]

optimizer = "adam"
loss ="mean_squared_error"


model = models.Sequential()

# Add a SimpleRNN layer
model.add(layers.SimpleRNN(512, activation='relu', input_shape=(769, 1), return_sequences=True))

# Add another SimpleRNN layer
model.add(layers.SimpleRNN(128, activation='relu'))

# Add a Dense (fully connected) layer
model.add(layers.Dense(32, activation='relu'))

# Add the output layer
model.add(layers.Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer=opt,
              loss=ls,
              metrics=['accuracy', 'precision', 'recall'])

# Display the model summary
model.summary()

accuracy = model.evaluate(X_test, Y_test)

precision = model.evaluate(X_test, Y_test)

recall = model.evaluate(X_test, Y_test)

print(accuracy)

print(precision)

print(recall)
