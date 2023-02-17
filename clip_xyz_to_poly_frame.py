from super_frame import *


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