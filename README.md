# Interactive Rename

## Description

This utility enables users to rename several files at once easily in a text
editor. It invokes the text editor of choice and populates it with filenames to
be modified. Just change the filenames in the editor, save, and quit, and the
renames will be reflected on the filesystem.

## Usage

	interactive-rename.py [-h] [-t] files [files ...]

### Arguments
- **files**
	files to be renamed
- **-t**, **--transaction**
	undo all operations when an error occurs
- **-v**, **--verbose**
	explain what is being done
- **-f**, **--force**
	overwrite files without confirmation

## Editor Settings

The program uses the `$EDITOR` environment variable to determine which editor
to use. If `$EDITOR` is not set, the `DEFAULT_EDITOR_COMMAND` at the beginning
of *interactive-rename.py* is used. You can change this variable to use your
favorite editor. Besides the editor name, additional parameters can be added to
`DEFAULT_EDITOR_COMMAND`. For example, to use emacs in terminal (`emacs -nw`),
change the line to something like this:

	DEFAULT_EDITOR_COMMAND = ["emacs", "-nw"]

Note that the the editor command must block until editing is complete, or the
rename will not work. One such example is the `gvim` command, which forks a new
process and return immediately.

If you are using gvim, please add the `-f` flag so that it will behave like a
blocking command:

	DEFAULT_EDITOR_COMMAND = ["gvim", "-f"]
