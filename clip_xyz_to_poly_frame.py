from las_shaper import clip_xyz_to_poly, intersect_using_spatial_index
from tkinter import ttk, StringVar, END
from tkinter.filedialog import asksaveasfilename, askopenfilename, askopenfilenames

class ClipXyzToPolyFrame(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text='CLIP XYZ TO POLYGON')

        self.xyz_input_path = StringVar()
        self.poly_input_path = StringVar()
        self.output_path = StringVar()
        self.__create_widgets()

    def __create_widgets(self):
        # xyz input entry
        self.xyz_input_entry = ttk.Entry(self)
        self.xyz_input_entry.grid(column=0, columnspan=2, row=0)
        self.xyz_input_entry.config(width=45)
        self.xyz_input_path.set("Input path (.xyz)")
        self.xyz_input_entry.insert(0, self.xyz_input_path.get())
        self.xyz_input_btn = ttk.Button(self, text="...", command=lambda: self.__get_input_path('.xyz'))
        self.xyz_input_btn.grid(column=2, row=0, sticky="W")
        self.xyz_input_btn.config(width=3)

        # polygon input entry
        self.poly_input_entry = ttk.Entry(self)
        self.poly_input_entry.grid(column=0, columnspan=2, row=1)
        self.poly_input_entry.config(width=45)
        self.poly_input_path.set("Input polygon path (.shp)")
        self.poly_input_entry.insert(0, self.poly_input_path.get())
        self.poly_input_btn = ttk.Button(self, text="...", command=lambda: self.__get_input_path('.shp'))
        self.poly_input_btn.grid(column=2, row=1, sticky="W")
        self.poly_input_btn.config(width=3)

        # output entry
        self.output_entry = ttk.Entry(self)
        self.output_entry.grid(column=0, columnspan=2, row=2)
        self.output_entry.config(width=45)
        self.output_path.set("Results path (.shp)")
        self.output_entry.insert(0, self.output_path.get())
        self.output_btn = ttk.Button(self, text="...", command=lambda: self.__set_output_path())
        self.output_btn.grid(column=2, row=2, sticky="W")
        self.output_btn.config(width=3)

        # run btn
        self.run_btn = ttk.Button(self, text="RUN", command=lambda: self.__run())
        self.run_btn.grid(column=0, columnspan=3, row=3)

        for widget in self.winfo_children():
            widget.grid(padx=0, pady=3)

    def __get_input_path(self, file_extension):
        if file_extension == '.xyz':
            inputpaths = askopenfilenames(title="Browse for .xyz files", filetypes=[("xyz file", "*.xyz")])
            if len(inputpaths) != 0:
                inputpaths = '; '.join(inputpaths)
                self.xyz_input_path.set(inputpaths)
                self.xyz_input_entry.delete(0, END)
                self.xyz_input_entry.insert(0, self.xyz_input_path.get())
        elif file_extension == '.shp':
            inputpath = askopenfilename(title="Browse for Shapefile", filetypes=[("Shapefile", "*.shp")])
            if len(inputpath) != 0:
                self.poly_input_path.set(inputpath)
                self.poly_input_entry.delete(0, END)
                self.poly_input_entry.insert(0, self.xyz_input_path.get())

    def __set_output_path(self):
        outputpath = asksaveasfilename(initialfile=f"Untitled.shp", filetypes=[("Shapefile", "*.shp")])
        if len(outputpath) != 0:
            self.output_path.set(outputpath)
            self.output_entry.delete(0, END)
            self.output_entry.insert(0, self.output_path.get())

    def __run(self):
        if self.xyz_input_path.get() != '' and self.poly_input_path.get() != '' and self.output_entry.get() != '':
            clip_xyz_to_poly(self.xyz_input_path.get(), self.output_entry.get(), self.poly_input_path.get())
        else:
            print('invalid input or output path')
