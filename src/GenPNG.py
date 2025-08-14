# ==== Module Imports ==================================================================================================
import argparse
from math import ceil
import numpy as np
from os import path
from PIL import Image


# ==== Constant Definitions ============================================================================================
DEFAULT_WIDTH = 512

MODE_GRAYSCALE = "L"
MODE_RGB       = "RGB"


# ==== Functions =======================================================================================================
def genPNG(input_file: str, output_file: str, width: int = DEFAULT_WIDTH, mode: str = MODE_GRAYSCALE) -> None:
    """ Convert an input binary file to a PNG representation.

    Args:
        input_file(str): Path to input binary to be converted to image.
        output_file(str): Destination file name image will be written to.
        width(int): Width output image should have.
        mode(str): Color mode of image. Should be either MODE_GRAYSCALE or MODE_RGB.
    """
    # Read the data as *serial* bytes (uint8)
    data: np.ndarray = np.fromfile(input_file, dtype=np.uint8)
    # Set the bytes required to define a pixel w/i the image
    if (mode == MODE_RGB):
        pixel_width = 3
    else:
        pixel_width = 1
    # Determine image dimensions based on input file size and pixel width
    file_size = path.getsize(input_file)
    if file_size >= width:
        height = ceil(file_size / width / pixel_width)
    else:
        height = 1
    # Pad bits to ensure length of array % pixel_width is 0
    pad_amount = ((width * height * pixel_width) - file_size)
    data = np.pad(data, pad_width=(0, pad_amount))
    # Reshape array based on pixel width
    if(pixel_width > 1):
        data = np.reshape(data, (height, width, pixel_width))
    else:
        data = np.reshape(data, (height, width))
    # Generate the image
    img = Image.fromarray(data, mode=mode)
    img.save(output_file)
    img.close()


# ==== Main ============================================================================================================
if __name__ == "__main__":
    argv = argparse.ArgumentParser(
        prog="Gen PNG", description="Script for generating images from binary files")
    argv.add_argument(
        "-i", "--input", help="Input file to be converted to image", required=True, type=str)
    argv.add_argument(
        "-o", "--output", help="Output file resulting image will be written to", required=True, type=str)
    argv.add_argument(
        "-w", "--width", help="Width of output image, in pixels", required=False, default=512, type=int)
    argv.add_argument(
        "-c", "--color", help="Color image should be generated instead of grayscale", action="store_true")
    argv = argv.parse_args()
    if (argv.color):
        mode = MODE_RGB
    else:
        mode = MODE_GRAYSCALE
    genPNG(argv.input, argv.output, argv.width, mode)
