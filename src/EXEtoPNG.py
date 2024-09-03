# ==== Module Imports ==================================================================================================
import argparse
import os
import multiprocessing
from typing import List

import GenPNG



# ==== Functions =======================================================================================================
def process_list(sub_file_list: List[str], in_dir: str, out_dir: str, width: int, colorMode: str) -> None:
    """
    Process a given list of binary files.
    :param sub_file_list: List of file paths.
    :param in_dir: Input directory.
    :param out_dir: Output Directory.
    :return: None
    """
    for f in sub_file_list:
        GenPNG.genPNG(f, f.replace(in_dir, out_dir), width, colorMode)


# ==== Main ============================================================================================================
if __name__ == "__main__":
    # Setup command line arguments
    cliArguments = argparse.ArgumentParser(prog="EXE to PNG", description="Convert .exe files into .png images.")
    cliArguments.add_argument("inputDir", help="Directory containing executable (.exe) files.")
    cliArguments.add_argument("outputDir", help="Directory to store output png files.")
    cliArguments.add_argument("--subprocesses", "-p", default=1, type=int)
    cliArguments.add_argument("--colorMode", "-c", default=GenPNG.MODE_GRAYSCALE, choices=["L", "RGB"])
    cliArguments.add_argument("--width", "-w", default=GenPNG.DEFAULT_WIDTH, type=int, help="Width of output images.")
    arguments = cliArguments.parse_args()

    # Make sure the given directories exist
    inputDirectory = arguments.inputDir
    outputDirectory = arguments.outputDir
    assert os.path.isdir(inputDirectory), f"Input directory `{inputDirectory}` is not a directory"
    assert os.path.isdir(outputDirectory), f"Output directory `{outputDirectory}` is not a directory"

    # Get the number of files in the input directory
    file_list = [x.path for x in os.scandir(inputDirectory) if os.path.isfile(x.path)]
    print(f"Found {len(file_list)} files to convert")

    # Initialize threads for parallel execution
    num_processes = arguments.subprocesses
    if(num_processes == 1):
        process_list(file_list, inputDirectory, outputDirectory, arguments.width, arguments.colorMode)
    else:
        print(f"Using {num_processes} threads")

        # Split the work evenly among the threads
        split_file_list = []
        for i in range(0, num_processes):
            split_file_list.append([])
        for i in range(0, len(file_list)):
            split_file_list[i % num_processes].append(file_list[i])

        # Add the work to the pool
        pool = multiprocessing.Pool(processes=num_processes)
        for sub_list in split_file_list:
            pool.apply_async(process_list, args=(sub_list, inputDirectory, outputDirectory, arguments.width, arguments.colorMode))

        # Start, do the work, and wait for results
        pool.close()
        pool.join()
