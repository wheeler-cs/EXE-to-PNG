# === Module Imports ===================================================================================================
from math import ceil
import numpy as np
from os import path
from PIL import Image
from sys import argv

# === Constant Definitions =============================================================================================
DEFAULT_WIDTH = 512


# === Functions ========================================================================================================
def gen_png_numpy(input_path: str, output_path: str, width: int = DEFAULT_WIDTH, mode: str = "L") -> None:
    """
    Convert an input binary file to a PNG representation.
    :param input_path: The path to the input binary.
    :param output_path: The path to the output.
    :param width: Width of the resulting image.
    :param mode: Either "L" or "RGB" (RGB just duplicates "L")
    :return: None
    """
    file_size: int = path.getsize(input_path)
    if file_size < width:
        height: int = 1
    else:
        height: int = ceil(file_size / width)

    # Read the data as *serial* bytes (uint8)
    data: np.ndarray = np.fromfile(input_path, dtype=np.uint8)

    # Pad the data to resize it
    pad_amount: int = ((width * height) - file_size)
    data = np.pad(
        data,
        pad_width=(0, pad_amount)
    )

    # Make it image shaped
    data = np.reshape(data, (height, width))

    # Use the appropriate mode
    if mode == "RGB":
        # Stack the data on itself to make the three channels
        data = np.dstack((data, data, data))
        img = Image.fromarray(data, mode="RGB")
    else:
        # Or just make it a PIL image
        img = Image.fromarray(data, mode="L")
    img.save(output_path + ".png")
    img.close()


# === Main =============================================================================================================
if __name__ == "__main__":
    gen_png_numpy(argv[1], argv[2])
