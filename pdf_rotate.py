import os
from os import path
from pdfrw import PdfReader, PdfWriter


DIRECTORY = r"R:\Digital Production Services\Department Projects\Donor Files"


def rotate_pdf(pdf_path, angle):
    angle = int(angle)
    assert angle % 90 == 0
    original = PdfReader(pdf_path)
    pages = original.pages
    for page in pages:
        page.Rotate = angle % 360
    output = PdfWriter(pdf_path)
    output.trailer = original
    output.write()


def main():
    for f in os.scandir(DIRECTORY):
        if f.is_dir():
            rotate_path = path.join(f.path, "rotate.txt")
            if path.exists(rotate_path):
                os.remove(rotate_path)
                for pdf in os.scandir(f.path):
                    if pdf.name.endswith(".pdf"):
                        rotate_pdf(pdf, -90)


if __name__ == '__main__':
    main()
