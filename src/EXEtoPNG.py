import GenPNG

from os import listdir, path
from sys import argv
import threading
from typing import List


def getDirectoryFiles(targetDirectory: str = "") -> List[str]:
    fileList = []
    # Get a list of files in a given directory
    for file in listdir(targetDirectory):
        fullFileName = targetDirectory + '/' + file
        # Only take note of files, not directories
        if(path.isfile(fullFileName)):
            fileList.append(file)
    return fileList


if __name__ == "__main__":
    inputDirectory = "input/"
    outputDirectory = "output/"
    fileList = getDirectoryFiles(inputDirectory)
    print("Found a total of " + str(len(fileList)) + " files to convert")
    for file in fileList:
        GenPNG.generateGrayScalePNG(inputDirectory + file, outputDirectory + file)
