from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import textwrap
import random

#load long list of words from file
def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = list(word_file.read().split())

    return valid_words

#generate random sentence like characters
def trim(words, t):
	text_rand = random.randint(1, len(words))

	text =  words.pop(text_rand)

	while (len(text) < 15):
		text_rand = random.randint(1, len(words))
		text = text + " " + words.pop(text_rand)
	
	text = text[:t] if len(text) > t else text
	return text

words = load_words()

text =  trim(words, 50)

font = ImageFont.truetype("arial", 40)

# get text size  
text_size = font.getsize(text)

#currently fixed image
source_img = Image.open("input.jpg").convert("RGBA")

x_start = random.randint(1,source_img.size[0])
y_start = random.randint(1,source_img.size[1])


#REMOVING BUTTON IDEA
# set button size + 10px margins
# button_size = (text_size[0]+20, text_size[1]+20)

# # create image with correct size and black background
# button_img = Image.new('RGBA', button_size, (0,0,0,0))

# put text on button with 10px margins
# button_draw = ImageDraw.Draw(button_img)
# button_draw.text((10, 10), text, font=font)

#currently fixed image
source_img = Image.open("input.jpg").convert("RGBA")
source_draw = ImageDraw.Draw(source_img)

#REMOVING BUTTON IDEA
# put button on source image in position (x_start, y_start)
#source_img.paste(button_img, (x_start, y_start))

source_draw.text((x_start, y_start), text, font=font)

print(text_size)


# save in new file
source_img = source_img.convert("RGB")
source_img.save("output.jpg", "JPEG")



#https://stackoverflow.com/questions/41405632/draw-a-rectangle-and-a-text-in-it-using-pil