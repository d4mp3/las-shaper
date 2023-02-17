from super_frame import *
from classification_codes import CLASSIFICATION_CODES


class ExtractLasClassFrame(SuperFrame):

    def __init__(self, main_window):
        self.input_path = StringVar()
        self.output_path = StringVar()
        self.root = main_window.root

    def create_frame(self, extract_las_class):
        frame = LabelFrame(self.root, text="Extract LAS class:", padx=5, pady=5)
        basic_pattern = self.create_basic_pattern(frame, ".las", ".las", self.input_path, self.output_path)

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
