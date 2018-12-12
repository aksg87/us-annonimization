import numpy as np
import png
import pydicom
from PIL import Image
from time import sleep
import os

def processDCM(imagePath):

	print("processing DCM " + imagePath)

	ds = pydicom.dcmread(imagePath)

	shape = ds.pixel_array.shape

	# Convert to float to avoid overflow or underflow losses.
	image_3d = ds.pixel_array.astype(float)

	# Rescaling grey scale between 0-255
	image_3d_scaled = (np.maximum(image_3d,0) / image_3d.max()) * 255.0

	# Convert to uint
	image_3d_scaled = np.uint8(image_3d_scaled)

	interval = 10 

	for x in range(1, shape[0], interval):

		print(os.path.basename(imagePath) + str(x))
		# Write the PNG file
		image_2d_scaled = image_3d_scaled[x,:,:]
		
		with open("./outputs/" + os.path.basename(imagePath) + str(x)+".png", 'wb') as png_file:
		    w = png.Writer(shape[2], shape[1], greyscale=True)
		    w.write(png_file, image_2d_scaled)
		 
		print("written")


#Assuming being run from /home/akshay/Dev/us-anonymize
rootDir = './thyroid-data/data/'
for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: %s' % dirName)
    for fname in fileList:
        print (dirName+fname)
        processDCM(dirName+fname)