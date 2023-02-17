from super_frame import *


class GetMaxHeightFrame(SuperFrame):

    def __init__(self, main_window):
        self.input_path = StringVar()
        self.output_path = StringVar()
        self.root = main_window.root


    def create_frame(self):
        frame = LabelFrame(self.root, text="Get max height from the features in shapefile:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, ".shp", ".shp", self.input_path, self.output_path)
        dem_input = Entry(frame, width=35, borderwidth=5)
        dsm_input = Entry(frame, width=35, borderwidth=5)
        dem_btn = Button(frame, text="...", padx=10, command=lambda: self.manage_path("open", dem_input))
        dsm_btn = Button(frame, text="...", padx=10, command=lambda: self.manage_path("open", dsm_input))
        dem_input.insert(0, "DEM input (.las)")
        dsm_input.insert(0, "DSM input (.las)")


        #grid positioning
        frame.grid(row=10, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        dem_input.grid(row=11, column=0, columnspan=2, padx=10, pady=10)
        dem_btn.grid(row=11, column=2)
        dsm_input.grid(row=12, column=0, columnspan=2, padx=10, pady=10)
        dsm_btn.grid(row=12, column=2)
        basic_pattern["input_entry"].grid(row=13, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=13, column=2)
        basic_pattern["output_entry"].grid(row=14, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=14, column=2)
        # basic_pattern["run_btn"].grid(row=15, column=0, columnspan=3, padx=10)