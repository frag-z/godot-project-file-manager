import os
import shutil
from glob import glob

for filename in glob('../**/project.godot', recursive=True):

    if filename == "../project.godot":
        continue # we must leave the root project file

    storage_filename = f"project_godot_files/{filename[3:]}"
    storage_dirname = os.path.dirname(storage_filename)

    os.makedirs(storage_dirname, exist_ok=True)
    print(filename, storage_filename)
    shutil.copyfile(filename, storage_filename)



