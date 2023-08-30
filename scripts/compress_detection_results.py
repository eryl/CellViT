import argparse
from functools import partial
from pathlib import Path
import multiprocessing
#import multiprocessing.dummy as multiprocessing
import zipfile

from tqdm import tqdm

CELL_DETECTIION_DIR = "cell_detection"
CELL_DETECTION_ARCHIVE = "cell_detection.zip"
FLAG_FILE_NAME = ".cell_detection_done"
DETECTION_FILES = ["cells.json", "cells.geojson", "cell_detection.json", "cell_detection.geojson", "cells.pt"]

def compress_cell_detection_results(cell_detection_dir: Path, remove_files=False):
    flag_file_path = cell_detection_dir / FLAG_FILE_NAME
    if flag_file_path.exists():
        with zipfile.ZipFile(cell_detection_dir / CELL_DETECTION_ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for file_name in DETECTION_FILES:
                file_path = cell_detection_dir / file_name
                if file_path.exists():
                    zf.write(file_path, file_name)
                    if remove_files:
                        file_path.unlink()


def filter_dir(postprocessing_dir: Path):
    if (postprocessing_dir / CELL_DETECTIION_DIR).exists():
        return postprocessing_dir / CELL_DETECTIION_DIR
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description="Script for collecting GeoJSON files from a folder structure and save them as a zip file.")
    parser.add_argument('root_directory', help="Base directory to scan for files. All subdirectories in the given file will searched.", type=Path)
    parser.add_argument('--remove-files', help="If this flag is set, the files will be removed after being added to the archive", action='store_true')
    args = parser.parse_args()

    #cell_detection_results_dirs = sorted(args.root_directory.glob(f"**/{CELL_DETECTIION_DIR}"))
    
    with multiprocessing.Pool() as pool:
        cell_detection_results_dirs = sorted([cell_detection_dir for cell_detection_dir in pool.imap_unordered(filter_dir, args.root_directory.iterdir()) if cell_detection_dir is not None])
        pbar = tqdm(desc="Compressing directories", total=len(cell_detection_results_dirs))
    
        compress_results_partial = partial(compress_cell_detection_results, remove_files=args.remove_files)
        for result in pool.imap_unordered(compress_results_partial, cell_detection_results_dirs):
            pbar.update()




if __name__ == '__main__':
    main()

