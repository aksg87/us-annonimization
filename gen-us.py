from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import textwrap
import random
import os

#load long list of words from file
def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = list(word_file.read().split())

    return valid_words

#generate random sentence like characters
def trim(trim_lenth, min_lenth):
	words = load_words()

	text_rand = random.randint(1, len(words))

	text =  words.pop(text_rand)

	while (len(text) < min_lenth):
		text_rand = random.randint(1, len(words))
		text = text + " " + words.pop(text_rand)
	
	text = text[:trim_lenth] if len(text) > trim_lenth else text
	return text

def drawCoordinates(x_s, y_s, imageDraw):
	font = ImageFont.truetype("arial", 10)
	coordAsStr = str(x_s) +" "+ str(y_s)

	imageDraw.text((x_s, y_s), coordAsStr, font=font)

def insertText_Image(text, font_size, imagePath, testCoordinates, coverText):

	font = ImageFont.truetype("arial", font_size)

	source_img = Image.open(imagePath).convert("RGBA")
	source_draw = ImageDraw.Draw(source_img)

	x_start = random.randint(0,round(source_img.size[0]))
	y_start = random.randint(0,round(source_img.size[1]))

	start_dim = (x_start,y_start)
	text_dim = font.getsize(text)
	rectCorner = tuple([sum(x) for x in zip(text_dim,start_dim)])

	c1 = random.randint(1,255)
	c2 = random.randint(1,255)
	c3 = random.randint(1,255)

	source_draw.text((x_start, y_start), text,fill=(c1,c2,c3,255), font=font)

	if testCoordinates:
		drawCoordinates(x_start, y_start, source_draw)

	if (coverText):
		source_draw.rectangle(start_dim+rectCorner, fill=128)

	# save in new file
	source_img = source_img.convert("RGB")
	fileName = "./generated-data/output" +os.path.basename(imagePath)
	source_img.save(fileName, "PNG")
	
	print(fileName + '\t' + str(start_dim + rectCorner))
	return source_img

def generate_image():

	folderPath = "/home/akshay/Dev/us-anonymize/outputs/"
	imageName = random.choice(os.listdir(folderPath)) 

	textSize = random.randint(10,50)
	trim_min = random.randint(3,30)
	trim_max = random.randint(trim_min,60)

	text =  trim(trim_max, trim_min)

	source_img = insertText_Image(text, textSize, folderPath+imageName, False, False) 


def obscure_image(imagePath, x_s, y_s, x_end, y_end):

	source_img = Image.open(imagePath).convert("RGBA")
	source_draw = ImageDraw.Draw(source_img)

	start_dim = (x_s,y_s)
	rectCorner = (x_end,y_end)

	source_draw.rectangle(start_dim+rectCorner, fill=128)

	# save in new file
	source_img = source_img.convert("RGB")
	fileName = "./generated-data/obscured_output" +os.path.basename(imagePath)
	source_img.save(fileName, "PNG")