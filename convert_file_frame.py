from tkinter import ttk, StringVar, IntVar, END
from tkinter.filedialog import asksaveasfilename, askopenfilename
from las_shaper import create_xyz_from_las, create_shp_from_xyz


class ConvertFileFrame(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text='CONVERT FILES')

        # vars for radio button handling and dynamic change of entries extensions
        self.radio_option = IntVar(value=0)

        # input/output paths vars
        self.input_path = StringVar(value=f"Input path (.las)")
        self.output_path = StringVar(value=f"Results path (.xyz)")

        self.__create_widgets()


    def __create_widgets(self):
        #radio buttons
        self.first_option = ttk.Radiobutton(self, text="XYZ from LAS", variable=self.radio_option, value=0, command=lambda: self.__extension_handler())
        self.first_option.grid(column=0, row=0, sticky='E', ipadx=5)
        self.second_option = ttk.Radiobutton(self, text="SHP from XYZ", variable=self.radio_option, value=1, command=lambda: self.__extension_handler())
        self.second_option.grid(column=1, row=0, sticky='W', ipadx=5)

        #input entry
        self.input_entry = ttk.Entry(self)
        self.input_entry.grid(column=0, columnspan=2, row=1)
        self.input_entry.config(width=45)
        self.input_entry.insert(0, self.input_path.get())
        self.input_btn = ttk.Button(self, text="...", command=lambda: self.__get_input_path())
        self.input_btn.grid(column=2, row=1, sticky="W")
        self.input_btn.config(width=3)

        #output entry
        self.output_entry = ttk.Entry(self)
        self.output_entry.grid(column=0, columnspan=2, row=2)
        self.output_entry.config(width=45)
        self.output_entry.insert(0, self.output_path.get())
        self.output_btn = ttk.Button(self, text="...", command=lambda: self.__set_output_path())
        self.output_btn.grid(column=2, row=2, sticky="W")
        self.output_btn.config(width=3)

        #run btn
        self.run_btn = ttk.Button(self, text="RUN", command=lambda: self.__run())
        self.run_btn.grid(column=0, columnspan=3, row=3)


        for widget in self.winfo_children():
            widget.grid(padx=0, pady=3)


    def __get_input_path(self):
        if int(self.radio_option.get()) == 0:
            inputpath = askopenfilename(title="Browse for .las file", filetypes=[("las file", "*.las")])
        elif int(self.radio_option.get()) == 1:
            inputpath = askopenfilename(title="Browse for .xyz file", filetypes=[("xyz file", "*.xyz")])

        if len(inputpath) != 0:
            self.input_path.set(inputpath)
            self.input_entry.delete(0, END)
            self.input_entry.insert(0, self.input_path.get())


    def __set_output_path(self):
        if int(self.radio_option.get()) == 0:
            outputpath = asksaveasfilename(initialfile=f"Untitled.xyz", filetypes=[("xyz file", "*.xyz")])
        elif int(self.radio_option.get()) == 1:
            outputpath = asksaveasfilename(initialfile=f"Untitled.shp", filetypes=[("shapefile", "*.shp")])

        if len(outputpath) != 0:
            self.output_path.set(outputpath)
            self.output_entry.delete(0, END)
            self.output_entry.insert(0, self.output_path.get())


    def __extension_handler(self):
        if int(self.radio_option.get()) == 0:
            self.input_path.set(f"Input path (.las)")
            self.output_path.set(f"Results path (.xyz)")

        elif int(self.radio_option.get()) == 1:
            self.input_path.set(f"Input path (.xyz)")
            self.output_path.set(f"Results path (.shp)")

        self.input_entry.delete(0, END)
        self.input_entry.insert(0, self.input_path.get())
        self.output_entry.delete(0, END)
        self.output_entry.insert(0, self.output_path.get())

    def __run(self):
        if self.input_entry.get() != '' and self.output_entry != '':
            if int(self.radio_option.get()) == 0:
                create_xyz_from_las(self.input_entry.get(), self.output_entry.get())
            elif int(self.radio_option.get()) == 1:
                create_shp_from_xyz(self.input_entry.get(), self.output_entry.get())
        else:
            print('invalid input or output path!')
