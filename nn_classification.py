# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
# %matplotlib inline

from sklearn.model_selection import train_test_split

pd_data = pd.read_csv('IoUs_416_Matlab_added.csv')
Is_car = pd.read_csv('Is_Car_GT.csv')
Deepstack = pd.read_csv('Deepstack_Results.csv')

pd_data = pd.merge(pd_data, Is_car, on='FileName')
# After removing some features
pd_data.pop('FileName')
pd_data.pop('ISSM')
pd_data.pop('RMSE')
pd_data.pop('FSIM')
pd_data.pop('PSNR')
pd_data.pop('SSIM')
pd_data.pop('EdgeEntropy')
print(pd_data)

dataset = pd_data.values
dataset_label = Deepstack.values
print(dataset)
dataset = preprocessing.normalize(dataset) # Normalizing the dataset

dataset = np.array(dataset)
dataset_label = np.array(dataset_label)

print(dataset.shape)
print(dataset_label.shape)
print(X_train.shape)

# Splitting the train_test data

X_train, X_test, Y_train, Y_test = train_test_split(dataset, dataset_label[:,3], test_size = 0.2)

# One Hot encoding for training class

train_class_A = []
train_class_B = []
train_class_C = []
train_class_D = []

for ii in range(Y_train.shape[0]):
    if Y_train[ii]>0 and Y_train[ii]<0.3:
      train_class_A.append(1)
    else:
      train_class_A.append(0)
    if Y_train[ii]>=0.3 and Y_train[ii]<0.5:
      train_class_B.append(1)
    else:
      train_class_B.append(0)
    if Y_train[ii]>=0.5 and Y_train[ii]<0.7:
      train_class_C.append(1)
    else:
      train_class_C.append(0)
    if Y_train[ii]>=0.7:
      train_class_D.append(1)
    else:
      train_class_D.append(0)

train_class_A = np.array((train_class_A))
train_class_B = np.array((train_class_B))
train_class_C = np.array((train_class_C))
train_class_D = np.array((train_class_D))

from sklearn.datasets import load_iris
from tensorflow.keras.layers import Dense
from tensorflow.keras import Input, Model
import tensorflow as tf

# Defining the NN layers

inputs = Input(shape=(10,), name='input') # Input layer
x = Dense(16, activation='relu', name='16')(inputs) # Hidden layer 1
x = Dense(32, activation='relu', name='32')(x) # Hidden layer 2

# Output layers
output1 = Dense(1, activation='softmax')(x)
output2 = Dense(1, activation='softmax')(x)
output3 = Dense(1, activation='softmax')(x)
output4 = Dense(1, activation='softmax')(x)

model = Model(inputs=inputs, outputs=[output1, output2, output3, output4])

model.compile(loss=['binary_crossentropy', 'binary_crossentropy', 'binary_crossentropy', 'binary_crossentropy'],
              optimizer='adam',
              metrics=['acc']) # Model details

history = model.fit(X_train, [train_class_A, train_class_B, train_class_C, train_class_D], epochs=1000, batch_size=28) # Fitting the model

# One Hot encoding for testing class

test_class_A = []
test_class_B = []
test_class_C = []
test_class_D = []

for ii in range(Y_test.shape[0]):
    if Y_test[ii]>0 and Y_test[ii]<0.3:
      test_class_A.append(1)
    else:
      test_class_A.append(0)
    if Y_test[ii]>=0.3 and Y_test[ii]<0.5:
      test_class_B.append(1)
    else:
      test_class_B.append(0)
    if Y_test[ii]>=0.5 and Y_test[ii]<0.7:
      test_class_C.append(1)
    else:
      test_class_C.append(0)
    if Y_test[ii]>=0.7:
      test_class_D.append(1)
    else:
      test_class_D.append(0)

test_class_A = np.array((test_class_A))
test_class_B = np.array((test_class_B))
test_class_C = np.array((test_class_C))
test_class_D = np.array((test_class_D))

model.evaluate(X_test, [test_class_A, test_class_B, test_class_C, test_class_D], verbose = 1) # Evaluating the model.
