import sys
from PIL import Image, ImageTk
import tkinter as tk


if len(sys.argv) == 2:
    path = sys.argv[1]
    root = tk.Tk()
    pil_image = Image.open(path)
    root.title(path)
    tk_image = ImageTk.PhotoImage(pil_image)
    label = tk.Label(root, image=tk_image, bg='white')
    label.pack(padx=5, pady=5)
    root.mainloop()
else:
    print('Usage: {} image_file_path'.format(sys.argv[0]))
