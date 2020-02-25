import argparse
from datetime import datetime
import os
import os.path
from openpyxl import Workbook
from openpyxl.styles import NamedStyle
import math


def format_datetime(dt_float):
    return datetime.fromtimestamp(dt_float)


def format_size(size_bytes):
    if size_bytes == 0:
        return ""
    else:
        return math.ceil(size_bytes / 1000)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_dir")

    args = parser.parse_args()
    target_dir = args.target_dir

    file_list = [(f.name, f.stat()) for f in os.scandir(target_dir)]

    content_list = [(f[0], f[1].st_size / 1000, format_datetime(f[1].st_ctime),
                     format_datetime(f[1].st_mtime)) for f in file_list]
    content_list.sort(key=lambda a: a[0])

    excelpath = os.path.join(target_dir, "Directory List.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.page_setup.fitToWidth = 1
    ws.append(("Name", "(Size (KB)", "Date Created", "Date Modified"))
    date_style = NamedStyle(name='date_style', number_format='DD/MM/YYYY HH:MM:MM')
    wb.add_named_style(date_style)
    for i in ('A', 'B', 'C', 'D'):
        ws.column_dimensions[i].width = '20'
    for i in range(len(content_list)):
        for j in range(4):
            cell = ws.cell(i+2, j+1)
            cell.value = content_list[i][j]

    wb.save(excelpath)


if __name__ == '__main__':
    main()
