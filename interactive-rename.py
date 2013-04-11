#!/usr/bin/env python
# Rename files with your favorite text editor

DEFAULT_EDITOR="vim"

import sys, os
import argparse
import tempfile
import subprocess

def get_editor():
    EDITOR = os.getenv("EDITOR")
    if EDITOR == None:
        EDITOR = DEFAULT_EDITOR
    return EDITOR

def rename_file(orig_name, new_name):
    try:
        os.rename(orig_name, new_name)
        print("%1s -> %2s" % (orig_name, new_name))
        return True
    except OSError as e:
        print("RENAME FAILED: %1s" % (e.strerror))
        return False

def rename_files(orig_files):
    fd = -1
    try:
        # create temporary file
        (fd, fpath) = tempfile.mkstemp(suffix="rename-files");

        # write file names to temporary file
        with open(fpath, "w") as fout:
            for f in orig_files:
                fout.write(f + "\n")

        # invoke the editor
        subprocess.call([get_editor(), fpath])

        # read the file back
        with open(fpath, "r") as fin:
            files = fin.read().splitlines()
        files = [f for f in files if f != ""] # remove empty lines

        # validate input
        if len(files) != len(orig_files):
            print("error: file count mismatch")
            return 1
        rename_count = 0
        for i in range(0, len(files)):
            if orig_files[i] != files[i]:
                if rename_file(orig_files[i], files[i]):
                    rename_count += 1 # succeed
        if rename_count == 0:
            print("nothing renamed")
        else:
            print("renamed %1d files" % (rename_count))
    except Exception as e:
        print("ERROR: %1s" % (e.strerror))
        pass
    finally:
        os.close(fd)
        os.remove(fpath)
        pass

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

