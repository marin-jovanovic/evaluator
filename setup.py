import tkinter
from tkinter import filedialog


def append_to_log(data):
    log = open("log.txt", "a")
    log.write(data + "\n")
    log.close()


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


def getSquareRoot():
    print("function call")


    # x1 = entry1.get()
    #
    # label1 = tkinter.Label(root, text=float(x1) ** 0.5)
    # canvas1.create_window(200, 230, window=label1)


def file_driver():
    append_to_log(file_chooser())

def dir_driver():
    append_to_log(dir_chooser())



if __name__ == '__main__':

    print("welcome to setup script")

    # print("select path to program")
    # append_to_log(file_chooser())
    #
    # print("select path to tests")
    # append_to_log(dir_chooser())



    root = tkinter.Tk()

    canvas1 = tkinter.Canvas(root, width=200, height=300)
    canvas1.pack()

    button1 = tkinter.Button(text='select path to program', command=file_driver)
    canvas1.create_window(100, 100, window=button1)

    button2 = tkinter.Button(text='select dir to tests', command=dir_driver)
    canvas1.create_window(100, 200, window=button2)

    root.mainloop()

    print()
    print("setup done, now start main")
