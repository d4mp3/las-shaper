from app import *
from gui import *


if __name__ == "__main__":
    gui = Gui()
    app = App()
    extract_las_class_frame = gui.extract_las_class_frame(app.extract_las_class)
    gui.root.mainloop()
