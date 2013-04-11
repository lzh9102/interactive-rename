# Interactive Rename

## Usage

	./interactive-rename.py <files>

## Description

The program invokes the text editor of choice and populates it with filenames
to be modified. Just change the filenames in the editor, save, and exit. The
renames will be reflected on the filesystem.

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
