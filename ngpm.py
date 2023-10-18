import os
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
    # project.godot(.blocked) files in the root dir create empty strings, remove those
    nested_project_paths = list(filter(lambda p: p != "", nested_project_paths))

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
    nested_project_paths.sort(key=lambda p: p.count("/"), reverse=True)
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

parser = argparse.ArgumentParser(prog='NGPM', description='Nested Godot Project Manager - A program which allows you to nest godot projects within themselves',
                                 epilog='this project is open source and open for improvements, for more information visit www.cuppajoeman.com')
parser.add_argument("-nest", action='store_true', help="The main argument to be used: runs the program with -bgpf and -mpn arguments, as described below")
parser.add_argument("-un-nest", action='store_true', help="Undoes any changes made by -nest: runs the program with -ugpf and -mpu arguments, as described below")
parser.add_argument("-bgpf", "--block-godot-project-files", action='store_true', help="Renames all project.godot files not in the root directory to project.godot.blocked, so that godot doesn't detect multiple project.godot files")
parser.add_argument("-ugpf", "--unblock-godot-project-files", action='store_true', help="After using -bgpf, this command renames any project.godot.blocked files back to project.godot")
parser.add_argument("-mpn", "--make-paths-nested", action='store_true', help="For every tscn file, if it is located in a nested project, then fix all paths in the file to be relative to the root project")
parser.add_argument("-mpu", "--make-paths-un-nested", action='store_true', help="After running -mpn, this command will rename all tscn located in nested projects to have their original file paths")

args = parser.parse_args()

if args.nest:
    block_nested_project_dot_godot_files()
    make_paths_nested(dry_run=False)
elif args.un_nest:
    unblock_nested_project_dot_godot_files()
    make_paths_un_nested(dry_run=False)
elif args.block_godot_project_files:
    block_nested_project_dot_godot_files()
elif args.unblock_godot_project_files:
    unblock_nested_project_dot_godot_files()
elif args.make_paths_nested:
    make_paths_nested()
elif args.make_paths_un_nested:
    make_paths_un_nested()
