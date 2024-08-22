# === Module Imports ===================================================================================================
from math import ceil
from os import  path
from PIL import Image
from sys import argv
from typing import List, Tuple


# === Constant Definitions =============================================================================================
DEFAULT_WIDTH = 512


# === Functions ========================================================================================================
def generateGrayScalePNG(inputFile: str, outputPNG: str, pngWidth: int = DEFAULT_WIDTH) -> None:
    pngPixels = generateGrayScalePixelData(inputFile)
    pngHeight = int(ceil(len(pngPixels) / pngWidth))
    newImage = Image.new("RGB", (pngWidth, pngHeight), color="black")
    newImage.putdata(pngPixels)
    newImage.save(outputPNG, "PNG")


def generateGrayScalePixelData(inputFile: str) -> List[int]:
    pixelArray = []
    fileSize = path.getsize(inputFile)
    with open(inputFile, "rb") as exeIn:
        # Iterate through file to get bytes in groups of 3
        for n in enumerate(range(0, fileSize)):
            pixelData = exeIn.read(1)
            # Convert bytes into tuple of (R, G, B)
            pixelData = (pixelData[0], pixelData[0], pixelData[0])
            pixelArray.append(pixelData)
    return pixelArray


def generatePNG(inputFile: str, outputPNG: str, pngWidth: int = DEFAULT_WIDTH) -> None:
    # Convert input file into pixels
    pngPixels = generatePixelData(inputFile)
    pngHeight = int(ceil(len(pngPixels) / pngWidth))
    # Create new PNG image using data from file
    newImage = Image.new("RGB", (pngWidth, pngHeight), color="white")
    newImage.putdata(pngPixels)
    newImage.save(outputPNG, "PNG")


def generatePixelData(inputFile: str) -> List[Tuple[int, int, int]]:
    pixelArray = []
    fileSize = path.getsize(inputFile)
    with open(inputFile, "rb") as exeIn:
        # Iterate through file to get bytes in groups of 3
        for n in range(0, ceil(fileSize / 3)):
            pixelData = exeIn.read(3)
            # Convert bytes into tuple of (R, G, B)
            match (len(pixelData)):
                # 255 substitutes for missing values
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


# === Main =============================================================================================================
if __name__ == "__main__":
    generateGrayScalePNG(argv[1], argv[2])
