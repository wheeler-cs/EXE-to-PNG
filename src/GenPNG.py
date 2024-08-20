from math import ceil
from os import path
from PIL import Image

PNG_WIDTH = 512

INPUT_FILE = "test/test.exe"

exeSize = path.getsize(INPUT_FILE)

height = int(ceil(exeSize / (PNG_WIDTH * 3))) + 1
width = PNG_WIDTH

size = (width, height)

img = Image.new("RGB", size, color="white")

pixelArray = []

with open(INPUT_FILE, "rb") as exeIn:
    for n in range(0, ceil(exeSize / 3)):
        pixelData = exeIn.read(3)
        match (len(pixelData)):
            case 1:
                pixelData = (pixelData[0], 255, 255)
            case 2:
                pixelData = (pixelData[0], pixelData[1], 255)
            case 3:
                pixelData = (pixelData[0], pixelData[1], pixelData[2])
            case _:
                pixelData = (255, 255, 255)
        pixelArray.append(pixelData)


img.putdata(pixelArray)
img.save("test/out2.png", "PNG")
