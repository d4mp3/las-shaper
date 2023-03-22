import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinter.filedialog import asksaveasfilename, askdirectory
from las2shp import *
from extract_las_class_frame import ExtractLasClassFrame
from merge_files_frame import MergeFilesFrame
from create_file_frame import CreateFileFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Las2Shp')
        self.geometry('850x350')
        self.resizable(0, 0)
        self.__create_widgets()


    def __create_widgets(self):
        # create the extract las class frame
        extract_las_class_frame = ExtractLasClassFrame(self)
        extract_las_class_frame.grid(column=0, row=0, padx=10, pady=5)

        # create the merge files frame
        merge_files_frame = MergeFilesFrame(self)
        merge_files_frame.grid(column=1, row=0, padx=10, pady=5)

        # create the create file frame
        create_files_frame = CreateFileFrame(self)
        create_files_frame.grid(column=0, row=1, padx=10, pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
