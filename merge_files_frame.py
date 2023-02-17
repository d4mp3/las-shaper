from super_frame import *


class MergeFilesFrame(SuperFrame):

    def __init__(self, main_window):
        self.input_path = StringVar()
        self.output_path = StringVar()
        self.root = main_window.root

        self.filetypes = {
            0: ["xyz files", ".xyz"],
            1: ["shp files", ".shp"],
        }

    def create_frame(self):
        frame = LabelFrame(self.root, text="Merge files:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, self.filetypes[0][0], self.filetypes[0][1],
                                                  self.input_path, self.output_path,)
        radio_pattern = self.create_radio_pattern(frame, basic_pattern, self.filetypes, ".xyz", ".shp")

        # run button
        # run_btn = Button(frame, text="RUN", width=5, padx=10,
        #                  command=lambda: extract_las_class(self.input_path.get(), self.output_path.get(), option.get()))

        # grid positioning
        frame.grid(row=0, column=3, columnspan=3, padx=10, pady=10)
        radio_pattern[".xyz"].grid(row=1, column=3, padx=10, sticky="e")
        radio_pattern[".shp"].grid(row=1, column=4, padx=10, sticky="w")
        basic_pattern["input_entry"].grid(row=2, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=2, column=5)
        basic_pattern["output_entry"].grid(row=3, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=3, column=5)
        # basic_pattern["run_btn"].grid(row=4, columnspan=3, column=3)
