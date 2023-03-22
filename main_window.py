from las2shp import *
from extract_las_class_frame import *
from merge_files_frame import *
from create_file_frame import *
from clip_xyz_to_poly_frame import *
from get_max_height_frame import *


class MainWindow():

    def __init__(self):
        self.root = Tk()
        self.root.title("Las2Shp")
        self.exit_button()
        self.console_log_frame()


    def exit_button(self):
        def handle_quiting():
            response = messagebox.askyesno('Quit program', "Are you sure?")

            if response == 1:
                self.root.quit()

        quit_btn = Button(self.root, text="EXIT", width=5, command=handle_quiting)
        quit_btn.grid(row=16, column=5, sticky="w", padx=10)


    def console_log_frame(self):
        frame = LabelFrame(self.root, text="Console log:", padx=5, pady=5)
        frame.grid(row=10, column=3, columnspan=3, rowspan=5, padx=10, pady=10, sticky="w")


    def event_viewer(self):
        log_viewer = Toplevel()
        log_viewer.title("Log Viewer")
        label = Label(log_viewer).grid()


if __name__ == "__main__":

    main_window = MainWindow()

    extract_las_class_frame = ExtractLasClassFrame(main_window)
    extract_las_class_frame.create_frame(extract_las_class)

    merge_files_frame = MergeFilesFrame(main_window)
    merge_files_frame.create_frame()

    create_files_frame = CreateFilesFrame(main_window)
    create_files_frame.create_frame()

    clip_xyz_to_poly_frame = ClipXyzToPolyFrame(main_window)
    clip_xyz_to_poly_frame.create_frame()

    get_max_height_frame = GetMaxHeightFrame(main_window)
    get_max_height_frame.create_frame()

    main_window.root.mainloop()

    class CreateFilesFrame(SuperFrame):

        def __init__(self, main_window):
            self.input_path = StringVar()
            self.output_path = StringVar()
            self.root = main_window.root

            self.filetypes = {
                0: [".las", ".xyz"],
                1: [".xyz", ".shp"],
            }

        def create_frame(self):
            frame = LabelFrame(self.root, text="Create files:", padx=5, pady=5)
            basic_pattern = self.create_basic_pattern(frame, self.filetypes[0][0], self.filetypes[0][1], self.input_path, self.output_path)
            radio_pattern = self.create_radio_pattern(frame, basic_pattern, self.filetypes, "XYZ from LAS",
                                                      "SHP from XYZ")

            # run button
            # run_btn = Button(frame, text="RUN", width=5, padx=10,
            #                  command=lambda: extract_las_class(self.input_path.get(), self.output_path.get(), option.get()))

            # grid positioning
            frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="w")
            radio_pattern["XYZ from LAS"].grid(row=6, column=0, padx=10, sticky="e")
            radio_pattern["SHP from XYZ"].grid(row=6, column=1, padx=10, sticky="w")
            basic_pattern["input_entry"].grid(row=7, column=0, columnspan=2, padx=10, pady=10)
            basic_pattern["input_btn"].grid(row=7, column=2)
            basic_pattern["output_entry"].grid(row=8, column=0, columnspan=2, padx=10, pady=10)
            basic_pattern["output_btn"].grid(row=8, column=2)
            # basic_pattern["run_btn"].grid(row=9, column=0, columnspan=3, padx=10)




class ClipXyzToPolyFrame(SuperFrame):

    def __init__(self, main_window):
        self.input_path = StringVar()
        self.output_path = StringVar()
        self.root = main_window.root


    def create_frame(self):
        frame = LabelFrame(self.root, text="Clip XYZ to POLYGON:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, ".xyz", ".shp", self.input_path, self.output_path)
        polygon_input = Entry(frame, width=35, borderwidth=5)
        polygon_input.insert(0, "Input polygon path (.shp)")
        polygon_input_btn = Button(frame, text="...", padx=10, command=lambda: self.manage_path("open", polygon_input))

        # grid positioning
        frame.grid(row=5, column=3, columnspan=3, padx=10, pady=10, sticky="w")
        basic_pattern["input_entry"].grid(row=6, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=6, column=5)
        polygon_input.grid(row=7, column=3, columnspan=2, padx=10, pady=10)
        polygon_input_btn.grid(row=7, column=5)
        basic_pattern["output_entry"].grid(row=8, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=8, column=5)
        # basic_pattern["run_btn"].grid(row=9, column=3, columnspan=3, padx=10)

