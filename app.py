import tkinter as tk
from tkinter import messagebox
from extract_las_class_frame import ExtractLasClassFrame
from merge_files_frame import MergeFilesFrame
from convert_file_frame import ConvertFileFrame
from clip_xyz_to_poly_frame import ClipXyzToPolyFrame
from get_max_height_frame import GetMaxHeightFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Las-Shaper')
        self.geometry('850x540')
        self.resizable(0, 0)
        self.__create_widgets()
        self.__quit_button()


    def __quit_button(self):
        def handle_quiting():
            response = messagebox.askyesno('Quit program', "Are you sure?")

            if response == 1:
                self.quit()

        quit_btn = tk.Button(self, text="EXIT", width=5, command=handle_quiting)
        quit_btn.grid(row=2, column=1, sticky="S", padx=10)

    def __create_widgets(self):
        # create the extract las class frame
        extract_las_class_frame = ExtractLasClassFrame(self)
        extract_las_class_frame.grid(column=0, row=0, padx=10, pady=5)

        # create the merge files frame
        merge_files_frame = MergeFilesFrame(self)
        merge_files_frame.grid(column=1, row=0, padx=10, pady=5)

        # create the convert file frame
        convert_file_frame = ConvertFileFrame(self)
        convert_file_frame.grid(column=0, row=1, padx=10, pady=5)

        # create the clip xyz to poly frame
        clip_xyz_to_poly_frame = ClipXyzToPolyFrame(self)
        clip_xyz_to_poly_frame.grid(column=1, row=1, padx=10, pady=5)

        # create the get max height from the features in shapefile frame
        get_max_height_frame = GetMaxHeightFrame(self)
        get_max_height_frame.grid(column=0, row=2, padx=10, pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
