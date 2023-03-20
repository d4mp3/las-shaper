from tkinter import ttk, StringVar, END
from tkinter.filedialog import asksaveasfilename, askopenfilenames
from classification_codes import CLASSIFICATION_CODES
from las2shp import extract_las_class


class ExtractLasClassFrame(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text='EXTRACT LAS CLASS')

        self.input_path = StringVar()
        self.output_path = StringVar()
        self.dropdown_option = StringVar()

        # #setup the grid layout manager
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(0, weight=3)
        # self.columnconfigure(0, weight=1)
        self.__create_widgets()


    def __create_widgets(self):
        #Label
        self.cassification_label = ttk.Label(self, text="Select classification code:")
        self.cassification_label.grid(column=0, row=0, sticky="W")

        #dropdown menu
        options = list(map(lambda x: str(x[0]) + ' ' + str(x[1]), CLASSIFICATION_CODES))
        self.dropdown_option.set(options[0])
        self.dropdown = ttk.OptionMenu(self, self.dropdown_option, *options)
        self.dropdown.grid(column=1, row=0, columnspan=2, sticky="W")
        self.dropdown.config(width=20)

        #input entry
        self.input_entry = ttk.Entry(self)
        self.input_entry.grid(column=0, columnspan=2, row=1)
        self.input_entry.config(width=45)
        self.input_path.set("Input path (.las)")
        self.input_entry.insert(0, self.input_path.get())
        self.input_btn = ttk.Button(self, text="...", command=lambda: self.__get_input_path())
        self.input_btn.grid(column=2, row=1, sticky="W")
        self.input_btn.config(width=3)

        #output entry
        self.output_entry = ttk.Entry(self)
        self.output_entry.grid(column=0, columnspan=2, row=2)
        self.output_entry.config(width=45)
        self.output_path.set("Results path (.las)")
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
        tuple_inputpaths = askopenfilenames(title="Browse for file", filetypes=[("las files", "*.las")])
        inputpaths = '; '.join(tuple_inputpaths)
        self.input_path.set(inputpaths)
        self.input_entry.delete(0, END)
        self.input_entry.insert(0, self.input_path.get())


    def __set_output_path(self):
        outputpath = asksaveasfilename(initialfile=f"Untitled.las", filetypes=[("las files", "*.las")])
        self.output_path.set(outputpath)
        self.output_entry.delete(0, END)
        self.output_entry.insert(0, self.output_path.get())


    def __run(self):
        if self.input_entry.get() != '' and self.output_entry != '':
            extract_las_class(self.input_entry.get(), self.output_entry.get(), self.dropdown_option.get()[0])
        else:
            print('invalid input or output path')
