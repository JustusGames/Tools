from tkinter import *
from tkinter import ttk
from tkinter import filedialog


window = Tk()
window.geometry("400x200")
window.title("Playlist Converter")
window.configure(bg="black")

ttk.Label(text="Playlist Converter v.01",foreground="white")

def open_file():
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select Source Playlist",
        filetypes=[("M3U Files","*.m3u")]
    )
    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected.")

open_file_button = Button(window,text="Open File", command=open_file)
open_file_button.pack(pady=64)

window.mainloop()


