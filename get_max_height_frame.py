from las2shp import get_max_value
from tkinter import ttk, StringVar, END
from tkinter.filedialog import asksaveasfilename, askopenfilename


class GetMaxHeightFrame(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text='ASSIGN MAX HEIGHT TO FEATURES IN SHAPEFILE')

        self.dem_input_path = StringVar()
        self.dsm_input_path = StringVar()
        self.shp_input_path = StringVar()
        self.output_path = StringVar()
        self.__create_widgets()

    def __create_widgets(self):
        # xyz input entry
        self.dem_input_entry = ttk.Entry(self)
        self.dem_input_entry.grid(column=0, columnspan=2, row=0)
        self.dem_input_entry.config(width=45)
        self.dem_input_path.set("DEM input (.xyz)")
        self.dem_input_entry.insert(0, self.dem_input_path.get())
        self.dem_input_btn = ttk.Button(self, text="...", command=lambda: self.__get_input_path('dem'))
        self.dem_input_btn.grid(column=2, row=0, sticky="W")
        self.dem_input_btn.config(width=3)

        # polygon input entry
        self.dsm_input_entry = ttk.Entry(self)
        self.dsm_input_entry.grid(column=0, columnspan=2, row=1)
        self.dsm_input_entry.config(width=45)
        self.dsm_input_path.set("DSM input (.xyz)")
        self.dsm_input_entry.insert(0, self.dsm_input_path.get())
        self.dsm_input_btn = ttk.Button(self, text="...", command=lambda: self.__get_input_path('dsm'))
        self.dsm_input_btn.grid(column=2, row=1, sticky="W")
        self.dsm_input_btn.config(width=3)

        # output entry
        self.shp_input_entry = ttk.Entry(self)
        self.shp_input_entry.grid(column=0, columnspan=2, row=2)
        self.shp_input_entry.config(width=45)
        self.shp_input_path.set("Shapefile input (.shp)")
        self.shp_input_entry.insert(0, self.shp_input_path.get())
        self.shp_input_btn = ttk.Button(self, text="...", command=lambda: self.__get_input_path())
        self.shp_input_btn.grid(column=2, row=2, sticky="W")
        self.shp_input_btn.config(width=3)

        # output entry
        self.output_entry = ttk.Entry(self)
        self.output_entry.grid(column=0, columnspan=2, row=3)
        self.output_entry.config(width=45)
        self.output_path.set("Results path (.shp)")
        self.output_entry.insert(0, self.output_path.get())
        self.output_btn = ttk.Button(self, text="...", command=lambda: self.__set_output_path())
        self.output_btn.grid(column=2, row=3, sticky="W")
        self.output_btn.config(width=3)

        # run btn
        self.run_btn = ttk.Button(self, text="RUN", command=lambda: self.__run())
        self.run_btn.grid(column=0, columnspan=3, row=4)

        for widget in self.winfo_children():
            widget.grid(padx=0, pady=3)

    def __get_input_path(self, las_model=None):
        if las_model:
            inputpath = askopenfilename(title="Browse for .xyz file", filetypes=[("xyz file", "*.xyz")])
            if las_model == "dem":
                if len(inputpath) != 0:
                    self.dem_input_path.set(inputpath)
                    self.dem_input_entry.delete(0, END)
                    self.dem_input_entry.insert(0, self.dem_input_path.get())
            elif las_model == "dsm":
                if len(inputpath) != 0:
                    self.dsm_input_path.set(inputpath)
                    self.dsm_input_entry.delete(0, END)
                    self.dsm_input_entry.insert(0, self.dsm_input_path.get())
        else:
            inputpath = askopenfilename(title="Browse for Shapefile", filetypes=[("Shapefile", "*.shp")])
            if len(inputpath) != 0:
                self.shp_input_path.set(inputpath)
                self.shp_input_entry.delete(0, END)
                self.shp_input_entry.insert(0, self.shp_input_path.get())

    def __set_output_path(self):
        outputpath = asksaveasfilename(initialfile=f"Untitled.shp", filetypes=[("Shapefile", "*.shp")])
        if len(outputpath) != 0:
            self.output_path.set(outputpath)
            self.output_entry.delete(0, END)
            self.output_entry.insert(0, self.output_path.get())

    def __run(self):
        if self.input_entry.get() != '' and self.output_entry != '':
            get_max_value(self.input_entry.get(), self.output_entry.get(), self.dropdown_option.get()[0])
        else:
            print('invalid input or output path')
