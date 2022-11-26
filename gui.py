from tkinter import *

class Gui():

    def __init__(self):
        self.root = Tk()
        # self.input_box = Entry(self.root, width=35, borderwidth=5)
        # self.input_box.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.root.title("Las2Shp")
        # self.label = Label(self.root)
        # self.browse_btn = Button(self.root, text="browse", padx=50, command=self.select_path)
        self.extract_las_class()


    def select_path(self):
        print("selecting path")


    def extract_las_class(self):
        label = Label(self.root, text='Extract LAS class:')
        input = Entry(self.root, width=35, borderwidth=5)
        input.insert(0, '[Input path]')
        output = Entry(self.root, width=35, borderwidth=5)
        output.insert(0, '[Output directory]')
        input_btn = Button(self.root, text='...', padx=10, command=self.select_path)
        output_btn = Button(self.root, text='...', padx=10, command=self.select_path)
        run_btn = Button(self.root, text='RUN', padx=10, command=self.select_path)

        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='w')
        input.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        input_btn.grid(row=1, column=2)
        output.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        output_btn.grid(row=2, column=2)
        run_btn.grid(row=3, column=0, sticky='w', padx=10)


    # def create_shp_from_xyz(self):
    #     label = Label(self.root, text='Create SHP from XYZ:')
    #     input = Entry(self.root, width=35, borderwidth=5)
    #     input.insert(0, '[Input path]')
    #     output = Entry(self.root, width=35, borderwidth=5)
    #     output.insert(0, '[Output directory]')
    #     input_btn = Button(self.root, text='...', padx=10, command=self.select_path)
    #     output_btn = Button(self.root, text='...', padx=10, command=self.select_path)
    #
    #     label.grid(row=0, column=3, columnspan=3, padx=10, pady=10, sticky='w')
    #     input.grid(row=1, column=3, columnspan=2, padx=10, pady=10)
    #     input_btn.grid(row=1, column=5)
    #     output.grid(row=2, column=3, columnspan=2, padx=10, pady=10)
    #     output_btn.grid(row=2, column=5)
    #
    # #
    #
    #
    # def create_xyz_from_las(self):
    #     label = Label(self.root, text='Create XYZ from LAS:')
    #     input = Entry(self.root, width=35, borderwidth=5)
    #     input.insert(0, '[Input path]')
    #     output = Entry(self.root, width=35, borderwidth=5)
    #     output.insert(0, '[Output directory]')
    #     input_btn = Button(self.root, text='...', padx=10, command=self.select_path)
    #     output_btn = Button(self.root, text='...', padx=10, command=self.select_path)
    #
    #     label.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='w')
    #     input.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    #     input_btn.grid(row=4, column=2)
    #     output.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    #     output_btn.grid(row=5, column=2)
    #
    #
    #
    # def merge_shp_files(self, inpath, outpath):
    #     label = Label(self.root, text='Merge SHP files:')
    #     input = Entry(self.root, width=35, borderwidth=5)
    #     input.insert(0, '[Input path]')
    #     output = Entry(self.root, width=35, borderwidth=5)
    #     output.insert(0, '[Output directory]')
    #     input_btn = Button(self.root, text='...', padx=10, command=self.select_path)
    #     output_btn = Button(self.root, text='...', padx=10, command=self.select_path)
    #
    #     label.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='w')
    #     input.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    #     input_btn.grid(row=4, column=2)
    #     output.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    #     output_btn.grid(row=5, column=2)

    def merge_xyz_files(self, inpath, outpath):
        ...


    def dem_handler(self, inpath, outpath, poly):
        # get path to poly geometry
        ...


    def get_max_value(self, poly, dem_points, bldg_points, outpath):
        ...



if __name__ == '__main__':
    gui = Gui()
    gui.root.mainloop()