'''
evaluate_model - model evaluation tools; loss/accuracy, confusion matrix, 
and classification frequency plots.
'''

import numpy as np 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import harry_plotter as hp
from sklearn.metrics import classification_report, confusion_matrix

# updating default plotting style.
hp.default(plt.rcParams)


def plot_loss_acc(history):
	'''
	Given model training history (output from keras.model.fit), this returns a quick plot
	containing training and validation loss and accuracy for comparison.
	'''
	# init figure
	fig, ax = plt.subplots(1, 2, figsize=(10, 4), sharex='row')

	# loss
	ax[0].set_title('Loss', fontsize=14)
	ax[0].plot(history.history['loss'], 'salmon', label='training')
	ax[0].plot(history.history['val_loss'], 'navy', label='validation')
	ax[0].legend(frameon=False, fontsize=12)
	ax[0].set_xlabel('Epoch', fontsize=12)
	hp.xtick_format(5, 1, ax=ax[0], format='%1.0f')

	# accuracy
	ax[1].set_title('Accuracy', fontsize=14)
	ax[1].plot(history.history['accuracy'], 'salmon', label='training')
	ax[1].plot(history.history['val_accuracy'], 'navy', label='validation')
	ax[1].legend(frameon=False, fontsize=12)
	ax[1].set_xlabel('Epoch', fontsize=12)

	return ax


def plot_confusion_matrix(y_test, y_predict, labels):
	'''
	Plotting confusion matrix with annotated (count) squares.
	'''

	# sklearn confusion matrix
	con_mat = confusion_matrix(y_test, y_predict)

	# plotting using seaborn heatmap, also can use plt.matshow
	fig = plt.figure(figsize=(8, 8))
	ax = fig.add_subplot()
	sns.set(font_scale=1) # for label size
	sns.heatmap(con_mat, annot=True, fmt='d', cmap='Blues', 
				xticklabels=labels, yticklabels=labels) 

	ax.set_xlabel('Prediction', fontsize=15)
	ax.set_ylabel('Actual value', fontsize=15)

	ax.set_xlim([0, np.unique(y_test).shape[0]])
	ax.set_ylim([0, np.unique(y_test).shape[0]])
	return ax