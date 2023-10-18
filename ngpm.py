import os
import shutil
import re
import argparse
from glob import glob

os.chdir("../")


def block_nested_project_dot_godot_files():
    for filename in glob('**/project.godot', recursive=True):
        base_project = "/" not in filename
        if not base_project:
            os.rename(filename, filename + ".blocked")


def unblock_nested_project_dot_godot_files():
    # note by the definition of the blocking function these files are never in the root project
    for filename in glob('**/project.godot.blocked', recursive=True):
        unblocked_filename = filename.rsplit('.', 1)[0]
        os.rename(filename, unblocked_filename)


def recursively_find_directories_containing_file(filename):
    matches = []
    for filename in glob(f'**/{filename}', recursive=True):
        matches.append(os.path.dirname(filename))
    return matches


def get_nested_project_paths():
    nested_project_paths = recursively_find_directories_containing_file("project.godot")
    nested_project_paths.extend(recursively_find_directories_containing_file("project.godot.blocked"))
    return nested_project_paths


def path_is_inside_nested_project(nested_project_paths, query_path):
    for nested_project_path in nested_project_paths:
        if nested_project_path in query_path:
            return True
    return False


def get_nested_project_file_is_in(nested_project_paths, query_path):
    """
    precondition: we know that this file is inside a nested project
    """
    for nested_project_path in nested_project_paths:
        if nested_project_path in query_path:
            return nested_project_path

    assert False  # you should not be able to reach this due to the precondition


def make_paths_nested(dry_run=True):
    nested_project_paths = get_nested_project_paths()

    for filename in glob('**/*.tscn', recursive=True):
        dir_name = os.path.dirname(filename)

        if path_is_inside_nested_project(nested_project_paths, dir_name):
            nested_project_file_is_in = get_nested_project_file_is_in(nested_project_paths, dir_name)

            f = open(filename, 'r')
            contents = f.read()
            path_corrected_contents = re.sub(r'"res://(.*?)"', rf'"res://{nested_project_file_is_in}/\1"', contents)

            if dry_run:
                print(f"changing {filename} to be:")
                print(path_corrected_contents)
            else:
                f = open(filename, 'w')
                f.write(path_corrected_contents)
                f.close()


def make_paths_un_nested(dry_run=True):
    nested_project_paths = get_nested_project_paths()

    for filename in glob('**/*.tscn', recursive=True):
        dir_name = os.path.dirname(filename)

        if path_is_inside_nested_project(nested_project_paths, dir_name):
            nested_project_file_is_in = get_nested_project_file_is_in(nested_project_paths, dir_name)

            f = open(filename, 'r')
            contents = f.read()
            path_corrected_contents = re.sub(rf'"res://{nested_project_file_is_in}/(.*?)"', rf'"res://\1"', contents)

            if dry_run:
                print(f"changing {filename} to be:")
                print(path_corrected_contents)
            else:
                f = open(filename, 'w')
                f.write(path_corrected_contents)
                f.close()

parser = argparse.ArgumentParser(prog='NGPM', description='Nested Godot Project Manager',
                                 epilog='Text at the bottom of help')
parser.add_argument("-bgpf", "--block-godot-project-files")
parser.add_argument("-ugpf", "--unblock-godot-project-files")
parser.add_argument("-mpn", "--make-paths-nested")
parser.add_argument("-mpu", "--make-paths-un-nested")

args = parser.parse_args()

if args.block_godot_project_files:
    block_nested_project_dot_godot_files()
elif args.ublock_godot_project_files:
    unblock_nested_project_dot_godot_files()
elif args.make_paths_nested:
    make_paths_nested()
elif args.make_paths_un_nested:
    make_paths_un_nested()

