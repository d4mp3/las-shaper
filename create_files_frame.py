from super_frame import *


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
