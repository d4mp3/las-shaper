from las2shp import *
from extract_las_class_frame import *
from merge_files_frame import *
from create_files_frame import *
from clip_xyz_to_poly_frame import *
from get_max_height_frame import *


class MainWindow():

    def __init__(self):
        self.root = Tk()
        self.root.title("Las2Shp")
        self.exit_button()
        self.console_log_frame()


    def exit_button(self):
        def handle_quiting():
            response = messagebox.askyesno('Quit program', "Are you sure?")

            if response == 1:
                self.root.quit()

        quit_btn = Button(self.root, text="EXIT", width=5, command=handle_quiting)
        quit_btn.grid(row=16, column=5, sticky="w", padx=10)


    def console_log_frame(self):
        frame = LabelFrame(self.root, text="Console log:", padx=5, pady=5)
        frame.grid(row=10, column=3, columnspan=3, rowspan=5, padx=10, pady=10, sticky="w")


    def event_viewer(self):
        log_viewer = Toplevel()
        log_viewer.title("Log Viewer")
        label = Label(log_viewer).grid()


if __name__ == "__main__":

    main_window = MainWindow()

    extract_las_class_frame = ExtractLasClassFrame(main_window)
    extract_las_class_frame.create_frame(extract_las_class)

    merge_files_frame = MergeFilesFrame(main_window)
    merge_files_frame.create_frame()

    create_files_frame = CreateFilesFrame(main_window)
    create_files_frame.create_frame()

    clip_xyz_to_poly_frame = ClipXyzToPolyFrame(main_window)
    clip_xyz_to_poly_frame.create_frame()

    get_max_height_frame = GetMaxHeightFrame(main_window)
    get_max_height_frame.create_frame()

    main_window.root.mainloop()

