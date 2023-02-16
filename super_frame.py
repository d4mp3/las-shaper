
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.filedialog import asksaveasfilename, askdirectory

class Widget():

    def __init__(self):
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


    def create_basic_pattern(self, label_frame, input_ext, output_ext, input_path, output_path):
        """
        Creates basic pattern with tkinter label frames for input/output entries and browse button.

        @param: label_frame tkinter LabelFrame object declared in specific widget module
        @param: input_ext input file extension
        @param: output_ext results file extension
        @param: input_path path to file(s)
        @param: output_path path to results
        """

        input_entry = Entry(label_frame, width=35, borderwidth=5)
        output_entry = Entry(label_frame, width=35, borderwidth=5)

        # input_path = self.paths[label_frame_type][0]
        # output_path = self.paths[label_frame_type][1]

        if input_ext in ["xyz files", "shp files"]:
            input_path.set(f"Input directory ({input_ext})")
            input_btn = Button(label_frame, text="...", padx=10, command=lambda: self.manage_path("set_dir", input_entry))
            output_path.set(f"Results path ({output_ext})")
        else:
            input_path.set(f"Input path ({input_ext})")
            input_btn = Button(label_frame, text="...", padx=10, command=lambda: self.manage_path("open", input_entry))
            output_path.set(f"Results path ({output_ext})")

        input_entry.insert(0, input_path.get())
        output_entry.insert(0, output_path.get())
        output_btn = Button(label_frame, text="...", padx=10, command=lambda: self.manage_path("save", output_entry, ext=output_ext))

        return {
                "input_entry": input_entry,
                "output_entry": output_entry,
                "input_btn": input_btn,
                "output_btn": output_btn,
                }


    def manage_path(self, action, entry, **kwargs):
        """
        Sets what type of action is needed to perform by browser button. Creates dict from action (keys) and specific
        method (values) for further settings of paths.

        @param: action type of action for tkinter button (set_dir, open, save)
        @param: entry tkinter Entry object
        @param: **kwargs possible output file extension
        """

        # declaration of desired files extensions
        extensions = (("las files", "*.las"), ("xyz files", "*.xyz"), ("shp files", "*.shp"), ("all files", "*.*"))

        action2function = {
            "open": self.set_input_path,
            "save": self.set_output_path,
            "set_dir": self.set_output_dir,
        }

        path = action2function[action](entry, *extensions, **kwargs)


    def set_input_path(self, entry, frame_type, *args, **kwargs):
        """
        Inserts input path for specific tkinter Entry object and sets variable with
        path for executions of functions from las2shp.py module.

        @param: entry tkinter Entry object
        @param: *args filetypes for tkinter filedialog
        @param: **kwargs file extension for saving. Ignored by this method
        """

        file_name = filedialog.askopenfilenames(title="Browse for file", filetypes=(args))
        file_names = '; '.join(file_name)

        if isinstance(file_names, str) and file_names != "":
            self.input_path.set(file_names)
            entry.delete(0, END)
            entry.insert(0, self.input_path.get())


    def set_output_path(self, entry, *args, **kwargs):
        """
        Inserts output path for specific tkinter Entry object and sets variable with
        path for executions of functions from las2shp.py module.

        @param: entry tkinter Entry object
        @param: *args filetypes for tkinter filedialog
        @param: **kwargs file extension for saving.
        """

        ext = (kwargs['ext'])
        file_name = asksaveasfilename(initialfile=f"Untitled{ext}", filetypes=args)

        if isinstance(file_name, str) and file_name != "":
            self.output_path.set(file_name)
            entry.delete(0, END)
            entry.insert(0, self.output_path.get())


    def set_output_dir(self, extensions, entry, frame_type, *args, **kwargs):
        """
        Inserts output directory path for specific tkinter Entry object and sets variable with
        path for executions of functions from las2shp.py module.

        @param: entry tkinter Entry object
        @param: *args filetypes for tkinter filedialog
        @param: **kwargs file extensions for saving. Ignored by this method
        """

        file_name = askdirectory()

        if isinstance(file_name, str) and file_name != "":
            self.output_path.set(file_name)
            entry.delete(0, END)
            entry.insert(0, self.output_path.get())


    def create_radio_pattern(self, label_frame, basic_pattern, extensions_dict, option1, option2):
        """
        Creates basic pattern with 2 radio buttons for Create Files widget and Merge Files widget.

        @param: label_frame tkinter LabelFrame object declared in specific widget module
        @param: basic_pattern reference to particular patterns contained by Create Files or Merge Files widget
        @param: extensions_dict predefined dict for dynamic changes purposes
        @param: option1 title for first radio button option
        @param: option2 title  for second radio button option
        """

        #files_type var is for predefined dict in constructor. It sets start value then that value is dynamical changed by ext_setter method.
        files_type = IntVar()
        files_type.set(0)
        first_btn = Radiobutton(label_frame, text=option1, variable=files_type, value=0,
                                command=lambda: self.ext_setter(files_type.get(), basic_pattern, extensions_dict))
        second_btn = Radiobutton(label_frame, text=option2, variable=files_type, value=1,
                                 command=lambda: self.ext_setter(files_type.get(), basic_pattern, extensions_dict))

        return {
            option1: first_btn,
            option2: second_btn,
        }


    def ext_setter(self, value, basic_pattern, extensions_dict):
        """
        Handles with dynamic changes of tkinter Entries object in wigets with multiple files methods (create files and merge files)

        @param: value value of radio button in this method it's key of some of predefined extensions_dict (self.merged_files_types, self.created_files_type )
        @param: basic_pattern reference to particular patterns contained by Create Files or Merge Files widget
        @param: extensions_dict predefined dict for dynamic changes purposes
        """

        if extensions_dict[str(value)][0] in ["xyz files", "shp files"]:
            self.input_path.set(f"Input directory ({extensions_dict[str(value)][0]})")
        else:
            self.input_path.set(f"Input path ({extensions_dict[str(value)][0]})")

        self.output_path.set(f"Results path ({extensions_dict[str(value)][1]})")

        basic_pattern["input_entry"].delete(0, END)
        basic_pattern["output_entry"].delete(0, END)
        basic_pattern["input_entry"].insert(0, self.input_path.get())
        basic_pattern["output_entry"].insert(0, self.output_path.get())