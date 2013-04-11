#!/usr/bin/env python
# Rename files with your favorite text editor

DEFAULT_EDITOR_COMMAND=["vim"]

import sys, os
import argparse
import tempfile
import subprocess

def get_editor_command(file):
    """ Return the command list to invoke the editor of choice. """
    EDITOR = os.getenv("EDITOR")
    if EDITOR == None:
        cmd = DEFAULT_EDITOR_COMMAND
    else:
        cmd = [EDITOR]
    return cmd + [file]

def rename_file(orig_name, new_name):
    """ Rename orig_name to new_name and print the results.
        Returns true if the rename succeeds, false otherwise.
    """
    if os.path.exists(new_name):
        print("RENAME FAILED: destination already exists: %1s" % (new_name))
        return False
    try:
        os.rename(orig_name, new_name)
        print("%1s -> %2s" % (orig_name, new_name))
        return True
    except Exception as e:
        print("RENAME FAILED: %1s -> %2s: %2s"
              % (orig_name, new_name, e.strerror))
        return False

def generate_tasklist(orig_files, dest_files):
    """ Generate a list containing tuples consisting of (src,dest) pairs. """
    tasklist = []
    for i in range(0, len(orig_files)):
        if orig_files[i] != dest_files[i]:
            tasklist.append((orig_files[i], dest_files[i]))
    return tasklist

def sort_tasklist(tasklist):
    """ Topological-sort the tasklist. This function assumes that
        there are no duplicates in the source filenames as well as the
        destination filenames. Returns the sorted tasklist.
    """
    source_dict = {}
    dest_dict = {}
    visited = {}
    # create lookup table
    for index, task in enumerate(tasklist):
        source_dict[task[0]] = index
        dest_dict[task[1]] = index
        visited[index] = False

    sorted_order = []

    # dfs
    for index, task in enumerate(tasklist):
        if visited[index]:
            continue
        st = [index]
        while st:
            tid = st[-1] # get the last item in the list
            if not visited[tid]: # enter node
                visited[tid] = True
                dest = tasklist[tid][1]
                if dest in source_dict:
                    # tasklist[tid] depends on another task
                    st.append(source_dict[dest]) # push the dependency onto stack
            else: # leave node
                st.pop()
                sorted_order.append(tasklist[tid])

    return sorted_order


def process_tasklist(tasklist):
    """ Rename files according to the tasklist.
        Returns the number of successful renames.
    """
    sorted_tasklist = sort_tasklist(tasklist)
    rename_count = 0
    for task in sorted_tasklist:
        if rename_file(task[0], task[1]):
            rename_count += 1
    return rename_count

def rename_files(orig_files):
    """ Write filenames in orig_files to a file, invoke the editor, and rename
        the files when the editor exits.
    """
    fd = -1
    try:
        # create temporary file
        (fd, fpath) = tempfile.mkstemp(suffix="rename-files");

        # write file names to temporary file
        with open(fpath, "w") as fout:
            for f in orig_files:
                fout.write(f + "\n")

        # invoke the editor
        subprocess.call(get_editor_command(fpath))

        # read the file back
        with open(fpath, "r") as fin:
            files = fin.read().splitlines()
        files = [f for f in files if f != ""] # remove empty lines

        # validate input
        if len(files) != len(orig_files):
            print("ERROR: file count mismatch")
            return 1

        # rename files
        tasklist = generate_tasklist(orig_files, files)
        rename_count = process_tasklist(tasklist)

        if rename_count == 0:
            print("nothing renamed")
        else:
            print("renamed %1d files" % (rename_count))
    except Exception as e:
        print("ERROR: %1s" % (e.strerror))
    finally:
        if fd >= 0:
            os.close(fd)
            os.remove(fpath)
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rename files with your favorite text editor.")
    parser.add_argument('files', type=str, nargs="+",
                      help="files to be renamed")
    args = parser.parse_args()

    files = args.files
    status = rename_files(files)
    sys.exit(status)

