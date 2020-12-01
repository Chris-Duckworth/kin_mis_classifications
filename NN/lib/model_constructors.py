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
    
    # Implementing 2D convolution with rectified linear unit activation. 
    # 32 convolutional filters, each with a size of 3x3.
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
    # Second convolution.
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    # Dropout to improve convergence / overfitting.
    model.add(Dropout(0.25))
    # Maximum Pooling.
    model.add(MaxPool2D(pool_size = (2, 2) ) )
    
    # Flattening. 
    model.add(Flatten() )
    
    # Couple of dense layers.
    model.add(Dense(128, activation = 'relu'))
    # Dropout to improve convergence / overfitting.
    model.add(Dropout(0.5))
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
    model = Sequential()
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


def build_tuning_sequential_FCN(hp):
	'''
	Building fully connected neural network with variable hyperparameters to tune 
	optimal FCN. 

	Model is configured for binary classification (binary cross-entropy) and adaptive 
	learning rate (ADAM).

	Input shape is pre-defined so kerastuner object is only input.
	'''

	model = Sequential()
	model.add(Flatten(input_shape=(32,32,1)))

	# Performing the tuning on the first dense layer. 
	# Tuning performed on number of units (number of output nodes) and dropout.
	hp_units = hp.Int('units_1', min_value = 16, max_value = 128, step = 16)
	model.add(Dense(units = hp_units, activation = 'relu'))
	hp_dropout = hp.Float('dropout_1', min_value = 0, max_value = 0.6, step = 0.1)
	model.add(Dropout(hp_dropout))

	# Second dense layer with tuning on unit size and dropout.
	hp_units = hp.Int('units_2', min_value = 64, max_value = 32, step = 32)
	model.add(Dense(units = hp_units, activation = 'relu'))
	hp_dropout = hp.Float('dropout_2', min_value = 0, max_value = 0.6, step = 0.1)
	model.add(Dropout(hp_dropout))

	# You know what time it is.
	hp_units = hp.Int('units_3', min_value = 16, max_value = 128, step = 16)
	model.add(Dense(units = hp_units, activation = 'relu'))
	hp_dropout = hp.Float('dropout_3', min_value = 0, max_value = 0.6, step = 0.1)
	model.add(Dropout(hp_dropout))

	# final layer with binary sigmoid classification.
	model.add(Dense(units = 1 , activation = 'sigmoid'))

	# Choosing an optimal learning rate for the optimizer.
	hp_learning_rate = hp.Choice('learning_rate', values = [1e-2, 1e-3, 1e-4, 1e-5]) 

	# Compiling each hypermodel with set of hyperparameters.
	model.compile(optimizer = keras.optimizers.Adam(learning_rate = hp_learning_rate),
				  loss = 'binary_crossentropy', 
				  metrics = ['accuracy'])

	return model


def build_tuning_sequential_CNN(hp):
	'''
	Building fully connected neural network with variable hyperparameters to tune 
	optimal FCN. 

	Model is configured for binary classification (binary cross-entropy) and adaptive 
	learning rate (ADAM).

	Input shape is pre-defined so kerastuner object is only input.
	'''
	model = Sequential()

	# first convolutional layer with number of filter choice.
	hp_filters = hp.Int('filters_1', min_value = 16, max_value = 64, step = 16)
	model.add(Conv2D(hp_filters, kernel_size=(3, 3), activation='relu', input_shape=(32, 32, 1)))
					 
	# second convolution.
	hp_filters = hp.Int('filters_2', min_value = 16, max_value = 64, step = 16)
	model.add(Conv2D(hp_filters, kernel_size=(3, 3), activation='relu'))

	# dropout.
	hp_dropout = hp.Float('dropout_1', min_value = 0, max_value = 0.6, step = 0.1)
	model.add(Dropout(hp_dropout))

	# Maximum Pooling.
	model.add(MaxPool2D(pool_size = (2, 2) ) )

	# Flattening. 
	model.add(Flatten() )

	# Dense layer with dropout.
	hp_units = hp.Int('units_1', min_value = 32, max_value = 128, step = 32)
	model.add(Dense(units = hp_units, activation = 'relu'))
	hp_dropout = hp.Float('dropout_2', min_value = 0, max_value = 0.6, step = 0.1)
	model.add(Dropout(hp_dropout))

	# final layer with binary sigmoid classification.
	model.add(Dense(units = 1, activation = 'sigmoid'))

	# Choosing an optimal learning rate for the optimizer.
	hp_learning_rate = hp.Choice('learning_rate', values = [1e-2, 1e-3, 1e-4]) 

	# Compiling each hypermodel with set of hyperparameters.
	model.compile(optimizer = keras.optimizers.Adam(learning_rate = hp_learning_rate),
				  loss = 'binary_crossentropy', 
				  metrics = ['accuracy'])

	return model
