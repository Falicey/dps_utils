import os
from os import path
import shutil
import argparse

FILE_FORMATS = (".tif",)


def clean_project_folder(dir_path):
    out_dir = path.join(dir_path, "out")
    if path.exists(out_dir):
        for f in os.scandir(dir_path):
            if f.name.endswith(FILE_FORMATS):
                os.remove(f.path)
        for f in os.scandir(out_dir):
            if f.name.endswith(FILE_FORMATS):
                os.rename(f.path, path.join(dir_path, f.name))
        shutil.rmtree(out_dir)


def batch_clean(dir_path):
    for batch_dir in os.scandir(dir_path):
        if batch_dir.is_dir():
            clean_project_folder(batch_dir.path)


def super_batch(dir_path):
    for batch_dir in os.scandir(dir_path):
        if batch_dir.is_dir():
            batch_clean(batch_dir.path)


def main():
    parser = argparse.ArgumentParser(description="Cleans the file structure of scan tailor output.")
    parser.add_argument("file_path", help="Project or batch directory.")
    parser.add_argument("-b", "--batch", action="store_true", help="Clean a batch of scan tailor projects.")
    parser.add_argument("-s", "--superbatch",
                        action="store_true", help="Clean a 2 level batch of scan tailor projects.")

    args = parser.parse_args()
    dir_path = args.file_path
    batch_mode = args.batch
    superbatch_mode = args.superbatch

    if superbatch_mode:
        super_batch(dir_path)
    if batch_mode:
        batch_clean(dir_path)
    else:
        clean_project_folder(dir_path)


if __name__ == '__main__':
    main()
