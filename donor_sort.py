import os.path

main_directory = r"R:\Digital Production Services\Department Projects\Donor Files"
tiff_directory = os.path.join(main_directory, "tiffs")
pdf_directory = os.path.join(main_directory, "pdfs")
jpg_directory = os.path.join(main_directory, "jpgs")

for dir1 in os.scandir(main_directory):
    if dir1.is_dir():
        for image in os.scandir(dir1):
            new_dir = None
            if image.name.endswith(".tif"):
                new_dir = tiff_directory
            elif image.name.endswith(".pdf"):
                new_dir = pdf_directory
            elif image.name.endswith(".jpg"):
                new_dir = jpg_directory
            if new_dir is not None:
                dest_path = os.path.join(new_dir, dir1.name, image.name)
                os.renames(image.path, dest_path)
