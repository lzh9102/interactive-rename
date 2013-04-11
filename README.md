# Interactive Rename

Rename files with your favorite text editor.

## Usage

	interactive-rename.py <files>

## Editor Settings

The program uses the `$EDITOR` environment variable to determine which editor
to use. If `$EDITOR` is not set, the `DEFAULT_EDITOR_COMMAND` at the beginning
of *interactive-rename.py* is used. You can change this variable to use your
favorite editor. Besides the editor name, additional parameters can be added to
`DEFAULT_EDITOR_COMMAND`. For example, to use emacs in terminal (`emacs -nw`),
change the line to something like this:

	DEFAULT_EDITOR_COMMAND = ["emacs", "-nw"]
