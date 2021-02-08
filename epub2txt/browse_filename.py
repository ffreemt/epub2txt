"""Browse to a file.

https://pythonspot.com/tk-file-dialogs/
filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
"""
# import sys
from pathlib import Path

import tkinter as Tkinter
from tkinter import filedialog as tkFileDialog


# fmt: off
def browse_filename(
        initialdir=Path.cwd(),
        title="Select a file",
        filetypes=(
            ("epub files", "*.epub"),
            ("all files", "*.*"),
        )
):
    # fmt: on
    '''Browse for a filename.'''
    root = Tkinter.Tk()
    root.withdraw()
    filename = tkFileDialog.askopenfilename(
        parent=root,
        initialdir=initialdir,
        title=title,
        filetypes=filetypes,
    )
    return filename
