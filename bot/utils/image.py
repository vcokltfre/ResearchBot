from PIL import Image
from math import ceil, sqrt

def getRGBfromI(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return red, green, blue

def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint

def make_image(text, filename):
    data = []
    for letter in text:
        r, g, b = getRGBfromI(ord(letter))
        data.append((r, g, b))
    data.append((0, 0, 0))
    size = ceil(sqrt(len(data)))
    img = Image.new("RGB", (size, size))
    img.putdata(data)
    img.save(filename)

def make_text(filename):
    data = Image.open(filename)
    pixels = list(data.getdata())
    complete = False
    output = ""
    for pixel in pixels:
        if not complete:
            if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
                complete = True
            else:
                output += chr(getIfromRGB((pixel[0], pixel[1], pixel[2])))
    return output