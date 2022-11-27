from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename, askdirectory
from classification_codes import CLASSIFICATION_CODES


class Gui():

    def __init__(self):
        self.root = Tk()
        self.root.title("Las2Shp")

        # variables
        self.input_path = StringVar()
        self.output_path = StringVar()
        self.merged_files_types = {
            '0': ['.xyz', 'xyz files'],
            '1': ['.shp', 'shp files'],
        }

        # frames
        self.extract_las_class_frame()
        self.merge_files_frame()
        self.create_files_frame()
        self.clip_xyz_to_poly_frame()
        self.get_max_height_frame()


        # quit_btn = Button(self.root, text="EXIT", command=self.root.quit)
        # quit_btn.grid(row=3, column=2, sticky="w", padx=10)


    # definition of common basic_pattern (in/out paths, run button)
    def create_basic_pattern(self, frame, file_extension, files_ext=''):
        input = Entry(frame, width=35, borderwidth=5)
        output = Entry(frame, width=35, borderwidth=5)

        if files_ext in ['xyz files', 'shp files']:
            self.input_path.set(f"Input directory ({files_ext})")
            input_btn = Button(frame, text="...", padx=10, command=lambda: self.get_path("set_dir", input))
            self.output_path.set(f"Results path ({file_extension})")
        else:
            self.input_path.set(f"Input path ({file_extension})")
            input_btn = Button(frame, text="...", padx=10, command=lambda: self.get_path("open", input))
            self.output_path.set(f"Results path ({file_extension})")


        input.insert(0, self.input_path.get())
        output.insert(0, self.output_path.get())
        output_btn = Button(frame, text="...", padx=10, command=lambda: self.get_path("save", output))
        run_btn = Button(frame, text="RUN", width=15, padx=10, command=self.event_viewer)

        return {
                "input": input,
                "output": output,
                "input_btn": input_btn,
                "output_btn": output_btn,
                "run_btn": run_btn,
                }


    def get_path(self, action, entry):
        extensions = (("las files", "*.las"), ("xyz files", "*.xyz"), ("shp files", "*.shp"), ("all files", "*.*"))

        action2function = {
            "open": self.set_input_path,
            "save": self.set_output_path,
            "set_dir": self.set_output_dir,
        }

        path = action2function[action](extensions, entry)


    def set_input_path(self, extensions, entry):
        file_name = filedialog.askopenfilename(title="Browse for file", filetypes=(extensions))

        if isinstance(file_name, str) and file_name != "":
            self.input_path.set(file_name)
            entry.delete(0, END)
            entry.insert(0, self.input_path.get())


    def set_output_path(self, extensions, entry):
        file_name = asksaveasfilename(initialfile="Untitled.las", defaultextension=".las", filetypes=extensions)

        if isinstance(file_name, str) and file_name != "":
            self.output_path.set(file_name)
            entry.delete(0, END)
            entry.insert(0, self.output_path.get())


    def set_output_dir(self, extensions, entry):
        file_name = askdirectory()

        if isinstance(file_name, str) and file_name != "":
            self.output_path.set(file_name)
            entry.delete(0, END)
            entry.insert(0, self.output_path.get())


    def event_viewer(self):
        log_viewer = Toplevel()
        log_viewer.title("Log Viewer")
        label = Label(log_viewer).grid()


    def extract_las_class_frame(self):
        frame = LabelFrame(self.root, text="Extract LAS class:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, ".las")

        # dropdown menu
        cassification_label = Label(frame, text="Select classification code:")
        code = StringVar()
        code.set(CLASSIFICATION_CODES[0])
        dropdown = OptionMenu(frame, code, *CLASSIFICATION_CODES)
        dropdown.config(width=15)

        # grid positioning
        cassification_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        dropdown.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        basic_pattern["input"].grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=2, column=2)
        basic_pattern["output"].grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=3, column=2)
        basic_pattern["run_btn"].grid(row=4, column=0, columnspan=3, padx=10)


    def create_radio_pattern(self, frame, ext_setter, text1, text2):
        files_type = IntVar()
        files_type.set(0)
        first_btn = Radiobutton(frame, text=text1, variable=files_type, value=0,
                              command=lambda: ext_setter(files_type.get()))
        second_btn = Radiobutton(frame, text=text2, variable=files_type, value=1,
                              command=lambda: ext_setter(files_type.get()))

        return {
            text1: first_btn,
            text2: second_btn,
        }


    def merge_files_frame(self):

        # function caller for radio buttons
        def caller(value):
            print(value)

        def setter(value):
            print(self.merged_files_types[str(value)])
            return self.merged_files_types[str(value)]


        frame = LabelFrame(self.root, text="Merge files:", padx=5, pady=5)
        print(self.merged_files_types['0'])
        basic_pattern = self.create_basic_pattern(frame, self.merged_files_types['0'][0], 'xyz files')
        radio_pattern = self.create_radio_pattern(frame, setter, ".xyz", ".shp")

        # grid positioning
        frame.grid(row=0, column=3, columnspan=3, padx=10, pady=10)
        radio_pattern['.xyz'].grid(row=1, column=3, padx=10, sticky="e")
        radio_pattern[".shp"].grid(row=1, column=4, padx=10, sticky="w")
        basic_pattern["input"].grid(row=2, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=2, column=5)
        basic_pattern["output"].grid(row=3, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=3, column=5)
        basic_pattern["run_btn"].grid(row=5, columnspan=3, column=3)


    def create_files_frame(self):

        # function caller for radio buttons
        def caller(value):
            print(value)


        frame = LabelFrame(self.root, text="Create files:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, "")
        radio_pattern = self.create_radio_pattern(frame, caller, "XYZ from LAS", "SHP from XYZ")

        # grid positioning
        frame.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        radio_pattern["XYZ from LAS"].grid(row=7, column=0, padx=10, sticky="e")
        radio_pattern["SHP from XYZ"].grid(row=7, column=1, padx=10, sticky="w")
        basic_pattern["input"].grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=8, column=2)
        basic_pattern["output"].grid(row=9, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=9, column=2)
        basic_pattern["run_btn"].grid(row=10, column=0, columnspan=3, padx=10)


    def clip_xyz_to_poly_frame(self):
        frame = LabelFrame(self.root, text="Clip XYZ to POLYGON:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, "")
        polygon_input = Entry(frame, width=35, borderwidth=5)
        polygon_input.insert(0, "Path to polygon shapefile")
        polygon_input_btn = Button(frame, text="...", padx=10, command=lambda: self.get_path("open", input))

        # grid positioning
        frame.grid(row=6, column=3, columnspan=3, padx=10, pady=10, sticky="w")
        basic_pattern["input"].grid(row=8, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=8, column=5)
        polygon_input.grid(row=9, column=3, columnspan=2, padx=10, pady=10)
        polygon_input_btn.grid(row=9, column=5)
        basic_pattern["output"].grid(row=10, column=3, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=10, column=5)
        basic_pattern["run_btn"].grid(row=11, column=3, columnspan=3, padx=10)


    def get_max_height_frame(self):
        frame = LabelFrame(self.root, text="Get max height:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, "")

        #grid positioning
        frame.grid(row=11, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        basic_pattern["input"].grid(row=12, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["input_btn"].grid(row=12, column=2)
        basic_pattern["output"].grid(row=13, column=0, columnspan=2, padx=10, pady=10)
        basic_pattern["output_btn"].grid(row=13, column=2)
        basic_pattern["run_btn"].grid(row=14, column=0, columnspan=3, padx=10)









if __name__ == "__main__":
    gui = Gui()
    gui.root.mainloop()