from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.filedialog import asksaveasfilename, askdirectory
from classification_codes import CLASSIFICATION_CODES
from app import *


class Gui():

    def __init__(self):
        self.root = Tk()
        self.root.title("Las2Shp")

        # definition of common variables
        self.input_path = StringVar()
        self.output_path = StringVar()
        self.merged_files_types = {
            "0": ["xyz files", ".xyz"],
            "1": ["shp files", ".shp"],
        }
        self.created_files_type = {
            "0": [".las", ".xyz"],
            "1": [".xyz", ".shp"],
        }

        # definition of frames
        # self.extract_las_class_frame()
        self.merge_files_frame()
        self.create_files_frame()
        self.clip_xyz_to_poly_frame()
        self.get_max_height_frame()
        self.console_log_frame()
        self.exit_button()


    # definition of common basic_pattern (in/out paths)
    def create_basic_pattern(self, frame, input_ext, output_ext):
        input_entry = Entry(frame, width=35, borderwidth=5)
        output_entry = Entry(frame, width=35, borderwidth=5)

        if input_ext in ["xyz files", "shp files"]:
            self.input_path.set(f"Input directory ({input_ext})")
            input_btn = Button(frame, text="...", padx=10, command=lambda: self.get_path("set_dir", input_entry))
            self.output_path.set(f"Results path ({output_ext})")
        else:
            self.input_path.set(f"Input path ({input_ext})")
            input_btn = Button(frame, text="...", padx=10, command=lambda: self.get_path("open", input_entry))
            self.output_path.set(f"Results path ({output_ext})")


        input_entry.insert(0, self.input_path.get())
        output_entry.insert(0, self.output_path.get())
        output_btn = Button(frame, text="...", padx=10, command=lambda: self.get_path("save", output_entry, ext=output_ext))

        return {
                "input_entry": input_entry,
                "output_entry": output_entry,
                "input_btn": input_btn,
                "output_btn": output_btn,
                }


    def create_radio_pattern(self, frame, ext_setter, basic_pattern, extensions_dict, text1, text2):
        files_type = IntVar()
        files_type.set(0)
        first_btn = Radiobutton(frame, text=text1, variable=files_type, value=0,
                                command=lambda: ext_setter(files_type.get(), basic_pattern, extensions_dict))
        second_btn = Radiobutton(frame, text=text2, variable=files_type, value=1,
                                 command=lambda: ext_setter(files_type.get(), basic_pattern, extensions_dict))

        return {
            text1: first_btn,
            text2: second_btn,
        }


    # dynamic settings for entry inserts extensions
    def ext_setter(self, value, basic_pattern, extensions_dict):
        if extensions_dict[str(value)][0] in ["xyz files", "shp files"]:
            self.input_path.set(f"Input directory ({extensions_dict[str(value)][0]})")
        else:
            self.input_path.set(f"Input path ({extensions_dict[str(value)][0]})")

        self.output_path.set(f"Results path ({extensions_dict[str(value)][1]})")

        basic_pattern["input_entry"].delete(0, END)
        basic_pattern["output_entry"].delete(0, END)
        basic_pattern["input_entry"].insert(0, self.input_path.get())
        basic_pattern["output_entry"].insert(0, self.output_path.get())


    def get_path(self, action, entry, **kwargs):
        extensions = (("las files", "*.las"), ("xyz files", "*.xyz"), ("shp files", "*.shp"), ("all files", "*.*"))

        action2function = {
            "open": self.set_input_path,
            "save": self.set_output_path,
            "set_dir": self.set_output_dir,
        }

        path = action2function[action](entry, *extensions, **kwargs)


    def set_input_path(self, entry, *args, **kwargs):
        file_name = filedialog.askopenfilenames(title="Browse for file", filetypes=(args))
        file_names = ', '.join(file_name)

        if isinstance(file_names, str) and file_names != "":
            self.input_path.set(file_names)
            entry.delete(0, END)
            entry.insert(0, self.input_path.get())


    def set_output_path(self, entry, *args, **kwargs):
        ext = (kwargs['ext'])
        file_name = asksaveasfilename(initialfile=f"Untitled{ext}", filetypes=args)

        if isinstance(file_name, str) and file_name != "":
            self.output_path.set(file_name)
            entry.delete(0, END)
            entry.insert(0, self.output_path.get())


    def set_output_dir(self, extensions, entry, *args, **kwargs):
        file_name = askdirectory()

        if isinstance(file_name, str) and file_name != "":
            self.output_path.set(file_name)
            entry.delete(0, END)
            entry.insert(0, self.output_path.get())


    def exit_button(self):

        def handle_quiting():
            response = messagebox.askyesno('Quit program', "Are you sure?")

            if  response == 1:
                self.root.quit()

        quit_btn = Button(self.root, text="EXIT", width=5, command=handle_quiting)
        quit_btn.grid(row=16, column=5, sticky="w", padx=10)


    def event_viewer(self):
        log_viewer = Toplevel()
        log_viewer.title("Log Viewer")
        label = Label(log_viewer).grid()


    def extract_las_class_frame(self, extract_las_class):
        frame = LabelFrame(self.root, text="Extract LAS class:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, ".las", ".las")

        # dropdown menu
        cassification_label = Label(frame, text="Select classification code:")
        option = StringVar()
        options = list(map(lambda x: str(x[0]) + ' ' + str(x[1]), CLASSIFICATION_CODES))
        option.set(options[0])
        dropdown = OptionMenu(frame, option, *options)
        dropdown.config(width=15)

        # run button
        run_btn = Button(frame, text="RUN", width=5, padx=10,
                         command=lambda: extract_las_class(self.input_path.get(), self.output_path.get(), option.get()))

        # grid positioning
        frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        cassification_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        dropdown.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        basic_pattern["input_entry"].grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=2, column=2)
        basic_pattern["output_entry"].grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=3, column=2)
        run_btn.grid(row=4, column=0, columnspan=3, padx=10)


    def merge_files_frame(self):

        # function radio_btn_caller for radio buttons
        def radio_btn_caller(value):
            print(value)


        frame = LabelFrame(self.root, text="Merge files:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, self.merged_files_types["0"][0], self.merged_files_types["0"][1])
        radio_pattern = self.create_radio_pattern(frame, self.ext_setter, basic_pattern, self.merged_files_types, ".xyz", ".shp")

        # grid positioning
        frame.grid(row=0, column=3, columnspan=3, padx=10, pady=10)
        radio_pattern[".xyz"].grid(row=1, column=3, padx=10, sticky="e")
        radio_pattern[".shp"].grid(row=1, column=4, padx=10, sticky="w")
        basic_pattern["input_entry"].grid(row=2, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=2, column=5)
        basic_pattern["output_entry"].grid(row=3, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=3, column=5)
        # basic_pattern["run_btn"].grid(row=4, columnspan=3, column=3)


    def create_files_frame(self):

        # function radio_btn_caller for radio buttons
        def radio_btn_caller(value):
            print(value)


        frame = LabelFrame(self.root, text="Create files:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, ".las", ".xyz")
        radio_pattern = self.create_radio_pattern(frame, self.ext_setter, basic_pattern, self.created_files_type, "XYZ from LAS", "SHP from XYZ")

        # grid positioning
        frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        radio_pattern["XYZ from LAS"].grid(row=6, column=0, padx=10, sticky="e")
        radio_pattern["SHP from XYZ"].grid(row=6, column=1, padx=10, sticky="w")
        basic_pattern["input_entry"].grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=7, column=2)
        basic_pattern["output_entry"].grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=8, column=2)
        # basic_pattern["run_btn"].grid(row=9, column=0, columnspan=3, padx=10)


    def clip_xyz_to_poly_frame(self):
        frame = LabelFrame(self.root, text="Clip XYZ to POLYGON:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, ".xyz", ".shp")
        polygon_input = Entry(frame, width=35, borderwidth=5)
        polygon_input.insert(0, "Input polygon path (.shp)")
        polygon_input_btn = Button(frame, text="...", padx=10, command=lambda: self.get_path("open", polygon_input))

        # grid positioning
        frame.grid(row=5, column=3, columnspan=3, padx=10, pady=10, sticky="w")
        basic_pattern["input_entry"].grid(row=6, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=6, column=5)
        polygon_input.grid(row=7, column=3, columnspan=2, padx=10, pady=10)
        polygon_input_btn.grid(row=7, column=5)
        basic_pattern["output_entry"].grid(row=8, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=8, column=5)
        # basic_pattern["run_btn"].grid(row=9, column=3, columnspan=3, padx=10)


    def get_max_height_frame(self):
        frame = LabelFrame(self.root, text="Get max height from the features in shapefile:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, ".shp", ".shp")
        dem_input = Entry(frame, width=35, borderwidth=5)
        dsm_input = Entry(frame, width=35, borderwidth=5)
        dem_btn = Button(frame, text="...", padx=10, command=lambda: self.get_path("open", dem_input,))
        dsm_btn = Button(frame, text="...", padx=10, command=lambda: self.get_path("open", dsm_input))
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


    def console_log_frame(self):
        frame = LabelFrame(self.root, text="Console log:", padx=5, pady=5)
        frame.grid(row=10, column=3, columnspan=3, rowspan=5, padx=10, pady=10, sticky="w")
