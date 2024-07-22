import os
from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter.font as tkFont

# Initialize file variable
file = None

# Function to handle opening a file
def open_file():
    global file
    file = fd.askopenfilename(defaultextension='.txt', filetypes=[('All Files', '*.*'), ("Text File", "*.txt")])

    if file != '':
        root.title(f"{os.path.basename(file)} - Notepad")
        text_area.delete(1.0, END)
        with open(file, "r") as file_:
            text_area.insert(1.0, file_.read())
    else:
        file = None

# Function to handle saving a file
def save_file():
    global file
    if file is None:
        file = fd.asksaveasfilename(initialfile='Untitled.txt', defaultextension='.txt',
                                    filetypes=[("Text File", "*.txt"), ("All Files", "*.*")])
    if file:
        with open(file, "w") as file_:
            file_.write(text_area.get(1.0, END))
        root.title(f"{os.path.basename(file)} - Notepad")

# Function to exit the application
def exit_application():
    root.destroy()

# Function to handle copying text
def copy_text():
    text_area.event_generate("<<Copy>>")

# Function to handle cutting text
def cut_text():
    text_area.event_generate("<<Cut>>")

# Function to handle pasting text
def paste_text():
    text_area.event_generate("<<Paste>>")

# Function to handle selecting all text
def select_all():
    text_area.tag_add('sel', '1.0', 'end')

# Function to handle deleting selected text
def delete_selected():
    text_area.delete('sel.first', 'sel.last')

# Function to display information about the text editor
def about_notepad():
    mb.showinfo("About Notepad", "This is just another Notepad, but this is better than all others")

# Function to display information about available commands
def about_commands():
    commands = """
Under the File Menu:
- 'New' clears the entire Text Area
- 'Open' clears text and opens another file
- 'Save' saves your current file 
- 'Save As' saves your file in another extension

Under the Edit Menu:
- 'Copy' copies the selected text to your clipboard
- 'Cut' cuts the selected text and removes it from the text area 
- 'Paste' pastes the copied/cut text
- 'Select All' selects the entire text
- 'Delete' deletes the selected text
"""

    mb.showinfo(title="All commands", message=commands, width=60, height=40)

# Function to apply bold style
def bold_text():
    current_tags = text_area.tag_names("sel.first")
    if "bold" in current_tags:
        text_area.tag_remove("bold", "sel.first", "sel.last")
    else:
        text_area.tag_add("bold", "sel.first", "sel.last")
        bold_font = tkFont.Font(text_area, text_area.cget("font"))
        bold_font.configure(weight="bold")
        text_area.tag_configure("bold", font=bold_font)

# Function to apply italic style
def italic_text():
    current_tags = text_area.tag_names("sel.first")
    if "italic" in current_tags:
        text_area.tag_remove("italic", "sel.first", "sel.last")
    else:
        text_area.tag_add("italic", "sel.first", "sel.last")
        italic_font = tkFont.Font(text_area, text_area.cget("font"))
        italic_font.configure(slant="italic")
        text_area.tag_configure("italic", font=italic_font)

# Function to apply underline style
def underline_text():
    current_tags = text_area.tag_names("sel.first")
    if "underline" in current_tags:
        text_area.tag_remove("underline", "sel.first", "sel.last")
    else:
        text_area.tag_add("underline", "sel.first", "sel.last")
        underline_font = tkFont.Font(text_area, text_area.cget("font"))
        underline_font.configure(underline=True)
        text_area.tag_configure("underline", font=underline_font)

# Function to change font size
def change_font_size(size):
    text_area.config(font=("Helvetica", size))

# Initialize Tkinter
root = Tk()
root.title("Untitled - Notepad")
root.geometry('800x500')

# Toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

# Toolbar buttons with text
button_open = Button(toolbar_frame, text="Open", command=open_file)
button_open.pack(side=LEFT, padx=5, pady=5)

button_save = Button(toolbar_frame, text="Save", command=save_file)
button_save.pack(side=LEFT, padx=5, pady=5)

button_copy = Button(toolbar_frame, text="Copy", command=copy_text)
button_copy.pack(side=LEFT, padx=5, pady=5)

button_cut = Button(toolbar_frame, text="Cut", command=cut_text)
button_cut.pack(side=LEFT, padx=5, pady=5)

button_paste = Button(toolbar_frame, text="Paste", command=paste_text)
button_paste.pack(side=LEFT, padx=5, pady=5)

button_bold = Button(toolbar_frame, text="Bold", command=bold_text)
button_bold.pack(side=LEFT, padx=5, pady=5)

button_italic = Button(toolbar_frame, text="Italic", command=italic_text)
button_italic.pack(side=LEFT, padx=5, pady=5)

button_underline = Button(toolbar_frame, text="Underline", command=underline_text)
button_underline.pack(side=LEFT, padx=5, pady=5)

# Font size options
font_size_menu = Menubutton(toolbar_frame, text="Font Size", relief=RAISED)
font_size_menu.menu = Menu(font_size_menu, tearoff=0)
font_size_menu["menu"] = font_size_menu.menu

for size in range(8, 33, 2):
    font_size_menu.menu.add_command(label=str(size), command=lambda size=size: change_font_size(size))

font_size_menu.pack(side=LEFT, padx=5, pady=5)

# Main text area with scroll bar
text_area = Text(root, font=("Helvetica", 12))
text_area.pack(fill=BOTH, expand=True)

scrollbar = Scrollbar(text_area)
scrollbar.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_area.yview)

# Menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = Menu(menu_bar, tearoff=False)
file_menu.add_command(label="New", command=lambda: text_area.delete(1.0, END))
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_application)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit menu
edit_menu = Menu(menu_bar, tearoff=False)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all)
edit_menu.add_command(label="Delete", command=delete_selected)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Help menu
help_menu = Menu(menu_bar, tearoff=False)
help_menu.add_command(label="About Notepad", command=about_notepad)
help_menu.add_command(label="About Commands", command=about_commands)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Start the main loop
root.mainloop()
