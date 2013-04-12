# Interactive Rename

This utility enables users to rename several files at once easily in a text
editor. It calculates the dependencies between renaming operations and
transforms them into a linear order that can be carried out one by one. For
example, renaming

	file1
	file2
	file3

into

	file2
	file3
	file4

will be carried out as

	rename file3 to file4
	rename file2 to file3
	rename file1 to file2

instead of

	rename file1 to file2  # error: file2 exists
	rename file2 to file3  # error: file3 exists
	rename file3 to file4

In case the oprations cannot be put into such a linear order (e.g. swaping two
filenames), the program will insert additional operations to make it possible.
For example, swapping names of file1 and file2 will be carried out like this:

	file2 -> file1.tmp
	file1 -> file2
	file1.tmp -> file1

## Usage

	./interactive-rename.py <files>

## Description

The program invokes the text editor of choice and populates it with filenames
to be modified. Just change the filenames in the editor, save, and exit, and
the renames will be reflected on the filesystem.

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
