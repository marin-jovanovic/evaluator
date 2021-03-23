import tkinter
from tkinter import filedialog


def append_to_log(data):
    log = open("log.txt", "a")
    log.write(data + "\n")
    log.close()


def app_chooser(message):
    print(message)
    root = tkinter.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    print("selected " + file_path)
    return file_path


def dir_chooser(message):
    root = tkinter.Tk()
    root.withdraw()
    dirname = filedialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
    return dirname


append_to_log(app_chooser("select path to program"))
append_to_log(dir_chooser("select path to tests"))

# import tkinter as tk

root = tkinter.Tk()

canvas1 = tkinter.Canvas(root, width=400, height=300)
canvas1.pack()

entry1 = tkinter.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def getSquareRoot():
    x1 = entry1.get()

    label1 = tkinter.Label(root, text=float(x1) ** 0.5)
    canvas1.create_window(200, 230, window=label1)


button1 = tkinter.Button(text='Get the Square Root', command=getSquareRoot)
canvas1.create_window(200, 180, window=button1)

root.mainloop()

# import Tkinter, tkFileDialog



print("setup done, now start main")