import tkinter
from tkinter import filedialog


def append_to_log(data):
    log = open("log.txt", "w")
    log.write(data + "\n")
    log.close()


def file_chooser():
    root = tkinter.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    print("selected " + file_path)
    return file_path


def dir_chooser():
    root = tkinter.Tk()
    root.withdraw()
    dirname = filedialog.askdirectory(parent=root, initialdir="/", title=
    'Please select a directory')
    return dirname


PROGRAM_PATH = ""
DIR_PATH = ""


def check_driver():
    from os import path
    global check

    if path.exists(PROGRAM_PATH) and path.exists(DIR_PATH):
        check.delete(0, tkinter.END)
        check.insert(0, "both paths exist, all ok, ready to exit by pressing X")

    elif path.exists(PROGRAM_PATH):
        check.delete(0, tkinter.END)
        check.insert(0, "no tests")

    elif path.exists(DIR_PATH):
        check.delete(0, tkinter.END)
        check.insert(0, "no program")


def file_driver():
    global PROGRAM_PATH
    temp = file_chooser()
    PROGRAM_PATH = temp
    global entry1
    entry1.delete(0, tkinter.END)
    entry1.insert(0, temp)

    check_driver()


def dir_driver():
    global DIR_PATH

    temp = dir_chooser()
    DIR_PATH = temp

    global entry2
    entry2.delete(0, tkinter.END)
    entry2.insert(0, temp)

    check_driver()


def on_closing():
    global root
    import tkinter.messagebox
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
        print("saving")

        append_to_log(PROGRAM_PATH + "\n" + DIR_PATH)

        root.destroy()


if __name__ == '__main__':
    print("welcome to setup script")
    print("if you do not see tkinter window go to log.txt")
    print("1. row = programs absolute path")
    print("2. row = directory with tests")
    print("3. row = empty")

    root = tkinter.Tk()

    canvas1 = tkinter.Canvas(root, width=1000, height=1000)
    canvas1.pack()

    entry1 = tkinter.Entry(root)
    entry1.place(x=10, y=10, width=500, height=100)

    entry2 = tkinter.Entry(root)
    entry2.place(x=10, y=300, width=500, height=100)

    check = tkinter.Entry(root)
    check.place(x=10, y=600, width=500, height=100)

    button1 = tkinter.Button(text='select path to program', command=file_driver)
    print(entry1.index(tkinter.INSERT))
    canvas1.create_window(110, 150, window=button1)

    button2 = tkinter.Button(text='select dir to tests', command=dir_driver)
    canvas1.create_window(110, 250, window=button2)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
    print("setup done, now start main")
