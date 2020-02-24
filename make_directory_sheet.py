import argparse
from datetime import datetime
import os
import os.path
import csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_dir")

    args = parser.parse_args()
    target_dir = args.target_dir

    file_list = [(f.name, f.stat()) for f in os.scandir(target_dir)]

    content_list = [(f[0], max(f[1].st_size // 1000, 0), datetime.fromtimestamp(f[1].st_mtime),
                     datetime.fromtimestamp(f[1].st_ctime)) for f in file_list]
    content_list.sort(key=lambda a: a[0])

    cvspath = os.path.join(target_dir, "Directory List.csv")

    with open(cvspath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel-tab')
        csvwriter.writerow(("Name", "Size (KB)", "Date Modified", "Date Created"))
        for c in content_list:
            csvwriter.writerow(c)


if __name__ == '__main__':
    main()
