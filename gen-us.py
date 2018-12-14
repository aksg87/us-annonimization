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
def getTextBlob(trim_lenth, min_lenth):
	words = load_words()

	text_rand = random.randint(1, len(words))

	text =  random.choice(words)

	while (len(text) < min_lenth):
		text_rand = random.randint(1, len(words))
		text = text + " " + random.choice(words)
	
	text = text[:trim_lenth] if len(text) > trim_lenth else text
	return text

def drawCoordinates(x_s, y_s, imageDraw):
	font = ImageFont.truetype("arial", 10)
	coordAsStr = str(x_s) +" "+ str(y_s)

	imageDraw.text((x_s, y_s), coordAsStr, font=font)

def insertText_Image(number):

	folderPath = "/home/akshay/Dev/us-anonymize/outputs/"
	imageName = random.choice(os.listdir(folderPath)) 
	imagePath = folderPath + imageName

	font_size = random.randint(10,50)
	trim_min = random.randint(1,15)
	trim_max = random.randint(trim_min,60)

	source_img = Image.open(imagePath).convert("RGBA")

	x_scaled = 256
	y_scaled = 256

	source_img = source_img.resize((x_scaled, y_scaled))

	source_draw = ImageDraw.Draw(source_img)

	text =  getTextBlob(trim_max, trim_min)

	font = ImageFont.truetype("arial", font_size)

	text_Img = Image.new('RGBA', source_img.size, (255,255,255,0))

	#coordinates of text when inserted
	x_start = round(random.randint(0,x_scaled)*.25)
	y_start = round(random.randint(0,y_scaled)*.75)
	start_dim = (x_start,y_start)
	text_dim = font.getsize(text)
	lowerRight = tuple([sum(x) for x in zip(text_dim,start_dim)])

	c1 = random.randint(1,255)
	c2 = random.randint(1,255)
	c3 = random.randint(1,255)
	c4 = random.randint(50,255)

	source_draw.text((x_start, y_start), text,fill=(c1,c2,c3,c4), font=font)

	d = ImageDraw.Draw(text_Img)
	d.text((x_start, y_start), text, fill=(c1,c2,c3,c4), font = font)

	source_img = Image.alpha_composite(source_img, text_Img)

	lowerRightNew = -1
	if(random.choice([True, False])):

		text =  getTextBlob(trim_max, trim_min)

		font = ImageFont.truetype("arial", font_size)

		text_Img = Image.new('RGBA', source_img.size, (255,255,255,0))

		#coordinates of text when inserted
		y_start2 = round(y_start + text_dim[1]*1.1)
		start_dim = (x_start-10,y_start-10)
		text_dim = font.getsize(text)
		lowerRightNew = tuple([sum(x)+10 for x in zip(lowerRight,(0,text_dim[1]))])

		c1 = random.randint(1,255)
		c2 = random.randint(1,255)
		c3 = random.randint(1,255)
		c4 = random.randint(50,255)

		source_draw.text((x_start, y_start2), text,fill=(c1,c2,c3,c4), font=font)

		d = ImageDraw.Draw(text_Img)
		d.text((x_start, y_start2), text, fill=(c1,c2,c3,c4), font = font)

		source_img = Image.alpha_composite(source_img, text_Img)


	if (lowerRightNew == -1):
		lowerRightNew = lowerRight


	if(random.choice([True, False])):
		source_img = source_img.transpose(Image.FLIP_LEFT_RIGHT)
		x_start = 256 - x_start
		lowerRightNew = tuple((256 - lowerRightNew[0], lowerRightNew[1]))

	fileName =  "./generated-data/"+str(number)+"_output" +os.path.basename(imagePath)
	source_img.save(fileName, "PNG")
	#source_img.show()

	obscure_image(source_img, x_start, y_start,	lowerRightNew[0],	lowerRightNew[1])
	




	return fileName + "\t" + str(start_dim + lowerRightNew) + "\n"

def generate_multipleImgs(number):

	dataout = open("./generated-data/all_outputdata.txt", "a")

	for x in range(1,number):

		dataout.write(insertText_Image(x))
		print('.', end='')

	dataout.close()


def obscure_image(source_img, x_s, y_s, x_end, y_end):

	source_draw = ImageDraw.Draw(source_img)

	start_dim = (x_s,y_s)
	lowerRight = (x_end,y_end)

	source_draw.rectangle((start_dim, lowerRight), fill=128)

	# save in new file
	source_img = source_img.convert("RGB")
	#fileName = "./generated-data/obscured_output" +os.path.basename(imagePath)
	#source_img.show()

generate_multipleImgs(50000)
