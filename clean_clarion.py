import os
from os import path
import shutil

for dir1 in os.scandir(r"R:\Digital Production Services\Department Projects\Clarion\test"):
    if dir1.is_dir():
        print(dir1.path)
        for dir2 in os.scandir(dir1.path):
            if dir2.is_dir():
                dir3 = path.join(dir2.path, "out")
                if path.exists(dir3):
                    print("good")
                    for old_image in os.scandir(dir2.path):
                        if old_image.name.endswith("tif"):
                            os.remove(old_image.path)
                    for new_image in os.scandir(dir3):
                        if new_image.name.endswith(".tif"):
                            os.rename(new_image.path, path.join(dir2.path, new_image.name))
                    shutil.rmtree(dir3)
