from PIL import Image # used for loading images
import numpy as np
import os # used for navigating to image path
import imageio # used for writing images
from random import shuffle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


DIR = './generated-data'
file_dict = {}

f = open("all_outputdata.txt", "r")
fileContents = f.read()
fileContents = fileContents.split('\n')

for i in range(len(fileContents)-1):
	fileContents[i] = fileContents[i].split('\t')
	fileContents[i][0] = os.path.basename(fileContents[i][0])
	fileContents[i][1] = np.asarray(eval(fileContents[i][1]))
	file_dict[fileContents[i][0]] = fileContents[i][1]

def get_size_statistics():
	  heights = []
	  widths = []
	  for img in os.listdir(DIR): 
	    path = os.path.join(DIR, img)
	    data = np.array(Image.open(path)) #PIL Image library
	    heights.append(data.shape[0])
	    widths.append(data.shape[1])
	  avg_height = sum(heights) / len(heights)
	  avg_width = sum(widths) / len(widths)
	  print("Average Height: " + str(avg_height))
	  print("Max Height: " + str(max(heights)))
	  print("Min Height: " + str(min(heights)))
	  print('\n')
	  print("Average Width: " + str(avg_width))
	  print("Max Width: " + str(max(widths)))
	  print("Min Width: " + str(min(widths)))

IMG_SIZE = 256

def load_data():
	train_data = []
	errors = 0
	for img in os.listdir(DIR):
		try:
			label = file_dict[os.path.basename(img)]
			path = os.path.join(DIR, img)
			img = Image.open(path)
			img = img.convert('L')
			img = img.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
			train_data.append([np.array(img), label])
		except KeyError:
			print(str(errors) + " Key ERROR: "+ os.path.join(DIR, img))
			errors = errors + 1
			continue

	shuffle(train_data)
	return train_data

data = load_data()


#not saving test data here
train_data, test_data = train_test_split(data,test_size=0.00)

plt.imshow(train_data[43][0], cmap = 'gist_gray')

trainImages = np.array([i[0] for i in train_data]).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
trainLabels = np.array([i[1] for i in train_data])



import keras
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers. normalization import BatchNormalization

import numpy as np

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import h5py

def create_model():
	model = Sequential()
	model.add(Conv2D(32, kernel_size = (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 1)))
	model.add(MaxPooling2D(pool_size=(2,2)))
	model.add(BatchNormalization())
	model.add(Conv2D(64, kernel_size=(3,3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2,2)))
	model.add(BatchNormalization())
	model.add(Conv2D(96, kernel_size=(3,3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2,2)))
	model.add(BatchNormalization())
	model.add(Conv2D(96, kernel_size=(3,3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2,2)))
	model.add(BatchNormalization())
	model.add(Conv2D(64, kernel_size=(3,3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2,2)))
	model.add(BatchNormalization())
	model.add(Dropout(0.2))
	model.add(Flatten())
	model.add(Dense(256, activation='relu'))
	model.add(Dropout(0.2))
	model.add(Dense(128, activation='relu'))
	model.add(Dropout(0.3))
	model.add(Dense(128, activation='relu'))
	model.add(Dropout(0.3))
	model.add(Dense(4, activation = 'linear'))
	return model


filepath="weights.best.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

# Fit the model
model.compile(loss='mean_squared_error', optimizer='adam', metrics = ['accuracy'])
history = model.fit(trainImages, trainLabels, validation_split=0.33, batch_size = 64, epochs = 100, callbacks=callbacks_list, verbose = 1)


def model_infer(model, imagePath):
	DIR = './generated-data'
	IMG_SIZE = 256

	img = Image.open(imagePath)
	img = img.convert('L')

	img.show()
	img = img.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)

	np_img = np.array(img)

	print("INPUT SHAPE and DISPLAY")
	print(np_img.shape)
	plt.imshow(np_img, cmap = 'gist_gray')
	#plt.show()

	np_img = np_img.reshape(-1,IMG_SIZE, IMG_SIZE, 1)

	print("PREDICTION:")
	pred = model.predict(np_img)
	print(pred)

	obscure_image(np_img, np.transpose(pred).tolist())

def obscure_image(np_img, coords):

	np_img = np_img.reshape(-IMG_SIZE,IMG_SIZE)
	plt.imshow(np_img, cmap = 'gist_gray')
	#plt.show()
	source_img = Image.fromarray(np_img)
	source_img.show()
	source_draw = ImageDraw.Draw(source_img)

	start_dim = tuple((coords[0][0],coords[1][0]))
	rectCorner = tuple((coords[2][0], coords[3][0]))

	print("DRAWING COORDINATES, (IMG, START, END):")
	print(source_img.size)
	print(start_dim)
	print(rectCorner)

	source_draw.rectangle(start_dim+rectCorner, fill=128)
	source_img.show()

