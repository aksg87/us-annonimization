import numpy as np
import png
import pydicom
from PIL import Image
from time import sleep

ds = pydicom.dcmread("/home/akshay/Downloads/thyroid/data/D13.dcm")

shape = ds.pixel_array.shape

# Convert to float to avoid overflow or underflow losses.
image_3d = ds.pixel_array.astype(float)

# Rescaling grey scale between 0-255
image_3d_scaled = (np.maximum(image_3d,0) / image_3d.max()) * 255.0

# Convert to uint
image_3d_scaled = np.uint8(image_3d_scaled)

interval = 10

for x in range(1,shape[0], interval):

	print(x)
	# Write the PNG file
	image_2d_scaled = image_3d_scaled[x,:,:]
	
	#im = Image.fromarray(image_2d_scaled)
	#im.save("/home/akshay/Dev/us-anonymize/outputs/image" + str(x) + ".jpeg" )
	with open("/home/akshay/Dev/us-anonymize/outputs/image" + str(x)+".png", 'wb') as png_file:
	    w = png.Writer(shape[2], shape[1], greyscale=True)
	    w.write(png_file, image_2d_scaled)
	    sleep(0.05)
	print("written")


