from math import ceil
from os import  path
from PIL import Image
from sys import argv


DEFAULT_WIDTH = 512


def generatePNG(inputEXE: str, outputPNG: str, pngWidth:int = DEFAULT_WIDTH) -> None:
    exeSize = path.getsize(inputEXE)
    pngHeight = int(ceil(exeSize / (pngWidth * 3)))
    newImage = Image.new("RGB", (pngWidth, pngHeight), color="white")
    pngPixels = generatePixelData(inputEXE)
    newImage.putdata(pngPixels)
    newImage.save(outputPNG, "PNG")


def generatePixelData(inputFile: str) -> []:
    pixelArray = []
    fileSize = path.getsize(inputFile)
    with open(inputFile, "rb") as exeIn:
        for n in range(0, ceil(fileSize / 3)):
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
    return pixelArray


if __name__ == "__main__":
    generatePNG(argv[1], argv[2])
