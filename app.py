import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinter.filedialog import asksaveasfilename, askdirectory
from las2shp import *
from extract_las_class_frame import ExtractLasClassFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Las2Shp')
        self.geometry('500x250')
        self.resizable(0, 0)

        # layout on the root window
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        # create the button frame
        extract_las_class_frame = ExtractLasClassFrame(self)
        extract_las_class_frame.grid(column=0, row=0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
