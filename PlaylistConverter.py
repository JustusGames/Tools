from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import os

window = Tk()
window.title("Playlist Converter")
window.configure(bg="grey")

source_tracks = []
flipped_tracks = []

selected_source_path_label = Label(window,
                             text="Selected Source Path",
                             fg="black",
                             bg="#808f96"
                             )

selected_target_path_label = Label(window,
                             text="Selected Target Path",
                             fg="black",
                             bg="#808f96"
                             )

find_replace_source_label = Label(window,
                             text="Source Target String",
                             fg="black",
                             bg="#808f96"
                             )

find_replace_target_label = Label(window,
                             text="Replace Target String",
                             fg="black",
                             bg="#808f96"
                             )

replace_source_entry_var = StringVar()
replace_source_entry_var.set("G:\\")
replace_target_entry_var = StringVar()
replace_target_entry_var.set("//<HDD0>//Music//")

find_replace_source_entry = Entry(window,
                                  textvariable = replace_source_entry_var,
                                  fg="#000000"
                                  )
find_replace_target_entry = Entry(window,
                                  textvariable = replace_target_entry_var,
                                  fg="#000000"
                                  )

source_path_var = StringVar()
source_path_var.set("Choose File")

target_path_var = StringVar()
target_path_var.set("Choose Target Directory")

target_playlist_name_var = StringVar()
target_playlist_name_var.set("")

path_not_selected_fg_color = "#808f96"
path_selected_fg_color = "#000000"

flip_slashes_bool = BooleanVar()


selected_source_path_display = Label(window,
                                     textvariable=source_path_var,
                                     justify=CENTER,
                                     width= 50,
                                     fg=path_not_selected_fg_color                                    
                                     )

selected_target_path_display = Label(window,
                                     textvariable=target_path_var,
                                     justify=CENTER,
                                     width= 50,
                                     fg=path_not_selected_fg_color                                    
                                     )                       

def read_m3u_basic(file_path):
    tracks = []
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    tracks.append(line)
                    
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    return tracks

def save_file(ptracks):
    full_new_target_path = target_path_var.get() + "/" + target_playlist_name_var.get()
    print(full_new_target_path)
    if os.path.exists(target_path_var.get()):
        with open(full_new_target_path, "w") as file:
            for line in ptracks:
                file.write(F"{line}\n")
    else:
        with open(full_new_target_path, "x") as file:
            for line in ptracks:
                file.write(F"{line}\n")

def open_file():
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select Source Playlist",
        filetypes=[("M3U Files","*.m3u")]
    )
    if file_path:
        print(f"Selected file: {file_path}")
        source_path_var.set(file_path)
        selected_source_path_display.config(fg=path_selected_fg_color)
    else:
        print("No file selected.")    
        selected_source_path_display.config(fg=path_not_selected_fg_color)

def open_target_folder():
    target_directory = filedialog.askdirectory(
        initialdir="/",
        title="Select Target Directory"
    )

    if target_directory:
        print(f"Selected Directory: {target_directory}")
        target_path_var.set(target_directory)
        selected_target_path_display.config(fg=path_selected_fg_color)
    else:
        print("No Target Directory")
        selected_target_path_display.config(fg=path_selected_fg_color)

def convert_playlist():
    m3u_source_file = source_path_var.get()
    target_playlist_name_var.set(os.path.basename(m3u_source_file))
    source_tracks = read_m3u_basic(m3u_source_file)
    replaced_tracks_var = replace_strings(source_tracks)
    if flip_slashes_bool.get() == True:
        toggle_flips_slashes(replaced_tracks_var)
        save_file(flipped_tracks)
    else:
        save_file(replaced_tracks_var)

def replace_strings(ptracks):
    source = replace_source_entry_var.get()
    target = replace_target_entry_var.get()
    return [line.replace(source,target) for line in ptracks]


def toggle_flips_slashes(ptracks):
    for line in ptracks:
        new_line = str(line).replace("\\","/")
        flipped_tracks.append(new_line)

def show_state():
    if flip_slashes_bool.get():
        print("checked")
    else:
        print("not_checked")

open_source_file_button = Button(window,text="Select Source Playlist", 
                          command=open_file,
                          fg="black",
                          bg="grey"
                          )

open_target_file_button = Button(window,text="Select Target Folder", 
                          command=open_target_folder,
                          fg="black",
                          bg="grey"
                          )

convert_playlist_button = Button(window,text="Convert Playlist", 
                          command=convert_playlist,
                          fg="black",
                          bg="grey"
                          )

switch_slashes_checkbutton = Checkbutton(window, 
                                         text="Flip Slashes",
                                         variable=flip_slashes_bool,
                                         onvalue=True,
                                         offvalue=False,
                                         command=show_state
                                         )

selected_source_path_label.grid(row=0,column=0,pady=2)
selected_source_path_display.grid(row=0,column=1,pady=2)
open_source_file_button.grid(row=0,column=2,sticky=E,pady=2)

selected_target_path_label.grid(row=1,column=0,pady=2)
selected_target_path_display.grid(row=1,column=1,pady=2)
open_target_file_button.grid(row=1,column=2,sticky=E,pady=2)

find_replace_source_label.grid(row=2,column=0)
find_replace_target_entry.grid(row=3,column=1)
find_replace_target_label.grid(row=3,column=0)
find_replace_source_entry.grid(row=2,column=1)
switch_slashes_checkbutton.grid(row=4,column=1)

convert_playlist_button.grid(row=5,column=1,pady=2)

window.mainloop()


