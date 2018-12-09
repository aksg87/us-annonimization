from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

FONT_PATH = "/home/akshay/Dev/deep-anpr/fonts/UKNumberPlate.ttf"


source_img = Image.open("input.jpg").convert("RGBA")


font = ImageFont.truetype("arial")

text = "very loooooooooooooooooong text"

# get text size
text_size = font.getsize(text)

# set button size + 10px margins
button_size = (text_size[0]+20, text_size[1]+20)

# create image with correct size and black background
button_img = Image.new('RGBA', button_size, "black")

# put text on button with 10px margins
button_draw = ImageDraw.Draw(button_img)
button_draw.text((10, 10), text, font=font)

# put button on source image in position (0, 0)
source_img.paste(button_img, (0, 0))

# save in new file
source_img = source_img.convert("RGB")
source_img.save("output.jpg", "JPEG")



#https://stackoverflow.com/questions/41405632/draw-a-rectangle-and-a-text-in-it-using-pil