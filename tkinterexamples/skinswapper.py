from tkinter import *
from tkinter import ttk
import os
import shutil, errno

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
def move():
	skin = variable.get()
	if not skin == "Please select a skin":
		print("Swapping to skin: ", skin)
		directory = os.path.dirname(os.path.realpath(__file__))
		source = os.path.join(directory, "SKINS", skin)
		#kill imgs folder
		if(os.path.exists("imgs")):
			shutil.rmtree("imgs")
		#kill cache folder
		if(os.path.exists("cache")):
			shutil.rmtree("cache")
		#kill sfx folder
		if(os.path.exists("se")):
			shutil.rmtree("se")
		#kill additional options
		if(os.path.exists("additional options")):
			shutil.rmtree("additional options")
		#kill introduction
		if(os.path.exists("[introduction]")):
			shutil.rmtree("[introduction]")
		#move skins over
		try:
			copytree(source, directory)
			print("Skin successfully swapped!")
		except OSError as exc:
			if exc.errno == errno.ENOTDIR:
				shutil.copy(src, dst)
			else: raise

#main window
root = Tk()
root.title("K-Shoot Mania Skin Swapper")
root.resizable(False, False)

#padding n stuff
mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#force size of 250x25
sizer = ttk.Frame(mainframe, width=250, height=25)

#list all options
options = os.listdir("SKINS")
options.append("Please select a skin")

variable = StringVar(mainframe)
variable.set(options[len(options)-1])
dropdown = OptionMenu(mainframe, variable, *options)
dropdown.grid(column=1, row=1)

#move button
buttun = ttk.Button(mainframe, text="Move", command=move).grid(column=0, row=1)

#pads around the items in the window
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

#enter event loop (makes everything run)
root.mainloop()