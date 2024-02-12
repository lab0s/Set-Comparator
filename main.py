from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt5 import uic
import sys
import os
app_path = os.path.dirname(os.path.abspath(__file__))
gui_path_main = os.path.join(app_path, "WindowUI.ui")
gui_path_error = os.path.join(app_path, "DialogError.ui")


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(gui_path_main, self)

class Error(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(gui_path_error, self)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    error = Error()
    error.show()

    sys.exit(app.exec())