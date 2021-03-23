import tkinter
from tkinter import filedialog


def append_to_log(data):
    log = open("log.txt", "a")
    log.write(data + "\n")
    log.close()

def get_log():
    for line in open("log.txt").readlines():
        print(line)

def file_chooser():
    # print(message)
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
        # check.insert(1, "no dir path")
        # print("Error occured during opening program\nCheck \"PROGRAM_PATH\" constant")
        # import sys
        # sys.exit()
    # if file(PROGRAM_PATH).
    # global entry1, entry2



def file_driver():
    global PROGRAM_PATH
    temp = file_chooser()
    PROGRAM_PATH = temp
    # append_to_log(temp)
    # append_to_log(file_chooser())
    global entry1
    entry1.delete(0, tkinter.END)
    entry1.insert(0, temp)

    check_driver()


def dir_driver():
    global DIR_PATH

    temp = dir_chooser()
    DIR_PATH = temp
    # append_to_log(dir_chooser())
    global entry2
    entry2.delete(0, tkinter.END)
    entry2.insert(0, temp)
    check_driver()

def on_closing():
    global root
    import tkinter.messagebox
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
        print("saving")
        with open("log.txt", "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(PROGRAM_PATH + "\n" + DIR_PATH + "\n")
            f.truncate()

        root.destroy()




if __name__ == '__main__':
    # global root, entry1, entry2
    # global canvas1
    print("welcome to setup script")
    print("if you do not see tkinter window go to log.txt")
    print("1. row = programs absolute path")
print("2. row = directory with tests")
    print("3. row = empty")

    root = tkinter.Tk()

    # root = tkinter.Tk()
    left_offset = 10

    canvas1 = tkinter.Canvas(root, width=1000, height=1000)
    canvas1.pack()

    entry1 = tkinter.Entry(root)
    entry1.place(x=left_offset,
                       y=10,
                       width=500,
                       height=100)

    entry2 = tkinter.Entry(root)
    entry2.place(x=left_offset,
                       y=300,
                       width=500,
                       height=100)

    check = tkinter.Entry(root)
    check.place(x=left_offset,
                       y=600,
                       width=500,
                       height=100)

    # entry2 = tkinter.Entry(root)

    # entry1 = tkinter.Entry(root)

    button1 = tkinter.Button(text='select path to program', command=file_driver)
    print(entry1.index(tkinter.INSERT))
    canvas1.create_window(left_offset + 100, 150, window=button1)

    # canvas1.create_window(100, 200, window=entry2)

    button2 = tkinter.Button(text='select dir to tests', command=dir_driver)
    canvas1.create_window(left_offset + 100, 250, window=button2)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
    print("setup done, now start main")


