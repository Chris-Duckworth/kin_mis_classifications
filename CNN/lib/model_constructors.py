'''
model_constructors - keras sequential API model constructors for use in vel field NNs.
'''

import keras 
import tensorflow as tf
from keras import Sequential
from keras.layers import Conv2D, Flatten, BatchNormalization, Dropout, MaxPool2D, Dense
import numpy as np


def build_fixed_sequential_CNN(input_shape):
    '''
    Building convolutional neural network with fixed hyperparameters to test basic 
    performance of CNN. 
    
    Model is configured for binary classification (binary cross-entropy) and adaptive 
    learning rate (ADAM).
    
    Input shape should be formatted with an additional dimensions 
    i.e. (img_size, img_size, 1).
    '''
    model = Sequential()
    
    # First convolutional block
    model.add(Conv2D(32, (3,3), strides = 1, padding = 'same',
    		  activation = 'relu' , input_shape = input_shape))
    model.add(BatchNormalization())
    model.add(MaxPool2D((2,2), strides = 2, padding = 'same'))
    model.add(Dropout(0.2))

    # Fully connect layer and output.
    model.add(Flatten())
    model.add(Dense(units = 128, activation = 'relu'))
    model.add(Dropout(0.2))
    model.add(Dense(units = 1, activation = 'sigmoid'))

    # Compiling model with binary crossentropy. 
    model.compile(optimizer = "adam" , 
    			  loss = 'binary_crossentropy', 
    			  metrics = ['accuracy'])
	
    return model


def build_fixed_sequential_FCN(input_shape):
    '''
    Building fully connected neural network with fixed hyperparameters to test basic 
    performance of FCN (multilayer perceptron). 
    
    Model is configured for binary classification (binary cross-entropy) and adaptive 
    learning rate (ADAM).
    
    Input shape is fine as (img_size, img_size), since is immediately flattened. 
    '''
    model = keras.models.Sequential()
    model.add(Flatten(input_shape=input_shape))
    
	# First fully connected layer
    model.add(Dense(128, activation="relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    
    # Further fully connected layers
    model.add(Dense(256, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.2))
    
    # final layer with binary sigmoid classification.
    model.add(Dense(units = 1 , activation = 'sigmoid'))
    
    model.compile(optimizer = "adam",
    			  loss = 'binary_crossentropy',
    			  metrics = ['accuracy'])

    return model
