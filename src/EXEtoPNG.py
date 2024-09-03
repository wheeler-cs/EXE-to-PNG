# ==== Module Imports ==================================================================================================
import os
import multiprocessing
import time
from typing import List

import GenPNG


# ==== Constant Definitions ============================================================================================
# RGB or L
CONVERSION_MODE = "L"


# ==== Functions =======================================================================================================
def process_list(sub_file_list: List[str], in_dir: str, out_dir: str) -> None:
    """
    Process a given list of binary files.
    :param sub_file_list: List of file paths.
    :param in_dir: Input directory.
    :param out_dir: Output Directory.
    :return: None
    """
    global CONVERSION_MODE
    for f in sub_file_list:
        GenPNG.gen_png_numpy(f, f.replace(in_dir, out_dir), mode=CONVERSION_MODE)


# ==== Main ============================================================================================================
if __name__ == "__main__":
    inputDirectory = "input/"
    outputDirectory = "output/"

    # Make sure the directories exist
    assert os.path.isdir(inputDirectory), f"Input directory `{inputDirectory}` is not a directory"
    assert os.path.isdir(outputDirectory), f"Output directory `{outputDirectory}` is not a directory"

    # Scan them, printing the file count
    file_list = [x.path for x in os.scandir(inputDirectory) if os.path.isfile(x.path)]
    print("Found a total of " + str(len(file_list)) + " files to convert")

    # Process initialization
    num_processes = multiprocessing.cpu_count() // 2    # Don't use all threads to save some memory
    pool = multiprocessing.Pool(processes=num_processes)

    # Split the work to divide to the threads
    if len(file_list) > num_processes:
        split_file_list = [
            file_list[i:i + num_processes]
            for i in range(0, len(file_list), num_processes)
        ]
    else:
        split_file_list = [
            file_list[i:i + num_processes]
            for i in range(0, len(file_list), 4)    # The step size can be decreased, but it doesn't matter much
        ]

    start = time.perf_counter()

    # Add the work to the pool
    for sub_list in split_file_list:
        pool.apply_async(process_list, args=(sub_list, inputDirectory, outputDirectory))

    # Start, do the work, and wait for results
    pool.close()
    pool.join()

    end = time.perf_counter()

    print(f"Conversion time: {end - start:.6f}s")
