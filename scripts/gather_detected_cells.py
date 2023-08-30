import argparse
from pathlib import Path
#import multiprocessing
import multiprocessing.dummy as multiprocessing
from functools import partial

import zipfile

from tqdm import tqdm

CELL_DETECTIION_DIR = "cell_detection"
CELL_DETECTION_ARCHIVE = "cell_detection.zip"
FLAG_FILE_NAME = ".cell_detection_done"
DETECTION_FILES = ["cells.json", "cells.geojson", "cell_detection.json", "cell_detection.geojson", "cells.pt"]


def main():
    parser = argparse.ArgumentParser(description="Script for collecting GeoJSON files from a folder structure and save them as a zip file.")
    parser.add_argument('root_directory', help="Base directory to scan for files. All subdirectories in the given file will searched.", type=Path)
    parser.add_argument('--include-file', help="Name of the file to include from the cell detection archives.", choices=DETECTION_FILES, default="cell_detection.geojson")
    parser.add_argument('--output-archive', help="Where to write the collected files.", type=Path)
    args = parser.parse_args()
    output_archive = args.output_archive
    if output_archive is None:
        output_archive = args.root_directory.parent / (args.include_file + '.zip')

    with multiprocessing.Pool(1) as pool:
        cell_detection_results_dirs = sorted([cell_detection_dir for cell_detection_dir in pool.imap_unordered(filter_dir, args.root_directory.iterdir()) if cell_detection_dir is not None])
        
        pbar = tqdm(desc="Compressing directories", total=len(cell_detection_results_dirs))

        with zipfile.ZipFile(output_archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            get_file_data = partial(extract_file_data, filename=args.include_file)
            for name, data in pool.imap_unordered(get_file_data, cell_detection_results_dirs):
                zf.writestr(name, data)
                pbar.update()


def extract_file_data(postprocessing_dir, filename="cell_detection.geojson"):
    archive_path = postprocessing_dir / CELL_DETECTIION_DIR / CELL_DETECTION_ARCHIVE
    image_name = postprocessing_dir.name + '_' + filename
    with zipfile.ZipFile(archive_path) as zf:
        data = zf.read(filename)
        return image_name, data


def filter_dir(postprocessing_dir: Path):
    archive_path = postprocessing_dir / CELL_DETECTIION_DIR / CELL_DETECTION_ARCHIVE
    if archive_path.exists():
        return postprocessing_dir
    else:
        return None
    

if __name__ == '__main__':
    main()