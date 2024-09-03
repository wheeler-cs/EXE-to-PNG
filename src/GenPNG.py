# ==== Module Imports ==================================================================================================
from math import ceil
import numpy as np
from os import path
from PIL import Image


# ==== Constant Definitions ============================================================================================
DEFAULT_WIDTH = 512

MODE_GRAYSCALE = "L"
MODE_RGB       = "RGB"


# ==== Functions =======================================================================================================
def genPNG(input_path: str, output_path: str, width: int = DEFAULT_WIDTH, mode: str = MODE_GRAYSCALE) -> None:
    """
    Convert an input binary file to a PNG representation.
    :param input_path: The path to the input binary.
    :param output_path: The path to the output.
    :param width: Width of the resulting image.
    :param mode: Either MODE_GRAYSCALE or MODE_RGB.
    :return: None
    """
    # Read the data as *serial* bytes (uint8)
    data: np.ndarray = np.fromfile(input_path, dtype=np.uint8)

    # Set the bytes required to define a pixel w/i the image
    pixel_width: int = 1
    if(mode == MODE_RGB):
        pixel_width = 3

    # Determine image dimensions based on input file size and pixel width
    file_size: int = path.getsize(input_path)
    height: int = 1
    if file_size >= width:
        height = ceil(file_size / width / pixel_width)

    # Pad bits to ensure length of array % pixel_width is 0
    pad_amount: int = ((width * height * pixel_width) - file_size)
    data = np.pad(data, pad_width=(0, pad_amount))

    # Reshape array based on pixel width
    if(pixel_width > 1):
        data = np.reshape(data, (height, width, pixel_width))
    else:
        data = np.reshape(data, (height, width))
    
    # Generate the image
    img = Image.fromarray(data, mode=mode)
    img.save(output_path + ".png")
    img.close()


# ==== Main ============================================================================================================
if __name__ == "__main__":
    print("This module is intended to support the conversion of .exe files to .png.")
    print("Run EXEtoPNG to convert executables to images.")
