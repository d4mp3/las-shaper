from tkinter import *
from tkinter import filedialog


class Gui():

    def __init__(self):
        self.root = Tk()
        self.root.title("Las2Shp")
        self.extract_las_class()
        self.merge_files()
        quit_btn = Button(self.root, text="EXIT", command=self.root.quit)
        quit_btn.grid(row=3, column=2, sticky="w", padx=10)


    def get_path(self):
        extensions = (("las files", "*.las"), ("xyz files", "*.xyz"),("shp files", "*.las") ,("all files", "*.*"))
        self.root = filedialog.askopenfile(title="Select a file", filetypes=(extensions))


    def extract_las_class(self):

        frame = LabelFrame(self.root, text="Extract LAS class:", padx=5, pady=5)
        input = Entry(frame, width=35, borderwidth=5)
        input.insert(0, "[Input path]")
        output = Entry(frame, width=35, borderwidth=5)
        output.insert(0, "[Output directory]")
        input_btn = Button(frame, text="...", padx=10, command=self.get_path)
        output_btn = Button(frame, text="...", padx=10, command=self.get_path)
        run_btn = Button(frame, text="RUN", padx=10, command=self.get_path)

        frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        input.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        input_btn.grid(row=1, column=2)
        output.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        output_btn.grid(row=2, column=2)
        run_btn.grid(row=3, column=0, sticky="w", padx=10)

    def event_viewer(self):
        log_viewer = Toplevel()
        log_viewer.title("Log Viewer")
        label = Label(log_viewer).grid()

    def merge_files(self):
        frame = LabelFrame(self.root, text="Merge Files:", padx=5, pady=5)
        input = Entry(frame, width=35, borderwidth=5)
        input.insert(0, "[Input path]")
        output = Entry(frame, width=35, borderwidth=5)
        output.insert(0, "[Output directory]")
        input_btn = Button(frame, text="...", padx=10, command=self.get_path)
        output_btn = Button(frame, text="...", padx=10, command=self.get_path)
        run_btn = Button(frame, text="RUN", padx=10, command=self.event_viewer)

        frame.grid(row=0, column=3, columnspan=3, padx=10, pady=10)
        input.grid(row=2, column=3, columnspan=2, padx=10, pady=10)
        input_btn.grid(row=2, column=5)
        output.grid(row=3, column=3, columnspan=2, padx=10, pady=10)
        output_btn.grid(row=3, column=5)
        run_btn.grid(row=4, column=3, sticky="w", padx=10)

        files_type = StringVar()
        files_type.set("xyz")
        xyz_btn = Radiobutton(frame, text=".xyz", variable=files_type, value="xyz",
                              command=lambda: clicked(files_type.get()))
        shp_btn = Radiobutton(frame, text=".shp", variable=files_type, value="shp",
                              command=lambda: clicked(files_type.get()))
        xyz_btn.grid(row=1, column=3, padx=10, sticky="e")
        shp_btn.grid(row=1, column=4, padx=10, sticky="w")

        def clicked(value):
            print(value)




    # def create_shp_from_xyz(self):
    #     label = Label(self.root, text="Create SHP from XYZ:")
    #     input = Entry(self.root, width=35, borderwidth=5)
    #     input.insert(0, "[Input path]")
    #     output = Entry(self.root, width=35, borderwidth=5)
    #     output.insert(0, "[Output directory]")
    #     input_btn = Button(self.root, text="...", padx=10, command=self.select_path)
    #     output_btn = Button(self.root, text="...", padx=10, command=self.select_path)
    #
    #     label.grid(row=0, column=3, columnspan=3, padx=10, pady=10, sticky="w")
    #     input.grid(row=1, column=3, columnspan=2, padx=10, pady=10)
    #     input_btn.grid(row=1, column=5)
    #     output.grid(row=2, column=3, columnspan=2, padx=10, pady=10)
    #     output_btn.grid(row=2, column=5)
    #
    # #
    #
    #
    # def create_xyz_from_las(self):
    #     label = Label(self.root, text="Create XYZ from LAS:")
    #     input = Entry(self.root, width=35, borderwidth=5)
    #     input.insert(0, "[Input path]")
    #     output = Entry(self.root, width=35, borderwidth=5)
    #     output.insert(0, "[Output directory]")
    #     input_btn = Button(self.root, text="...", padx=10, command=self.select_path)
    #     output_btn = Button(self.root, text="...", padx=10, command=self.select_path)
    #
    #     label.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="w")
    #     input.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    #     input_btn.grid(row=4, column=2)
    #     output.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    #     output_btn.grid(row=5, column=2)
    #
    #
    #
    # def merge_shp_files(self, inpath, outpath):
    #     label = Label(self.root, text="Merge SHP files:")
    #     input = Entry(self.root, width=35, borderwidth=5)
    #     input.insert(0, "[Input path]")
    #     output = Entry(self.root, width=35, borderwidth=5)
    #     output.insert(0, "[Output directory]")
    #     input_btn = Button(self.root, text="...", padx=10, command=self.select_path)
    #     output_btn = Button(self.root, text="...", padx=10, command=self.select_path)
    #
    #     label.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="w")
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



if __name__ == "__main__":
    gui = Gui()
    gui.root.mainloop()