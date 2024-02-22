from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QMessageBox
from PyQt5 import uic
import sys
import os
from enum import Enum
import sql_functions

app_path = os.path.dirname(os.path.abspath(__file__))
gui_path_main = os.path.join(app_path, "WindowUI.ui")
gui_path_error = os.path.join(app_path, "DialogError.ui")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(gui_path_main, self)

        self.pushButton_compare.clicked.connect(self.compare_clicked)
        self.pushButton_compare.setText("Compare")


    def compare_clicked(self):
        self.canItRun()
        
    def canItRun(self):
        first_input = self.lineEdit_first.text()
        second_input = self.lineEdit_second.text()

        self.error_list = []
        self.error_list.clear()

        # Create list of errors
        try:
            int(first_input)
            if sql_functions.is_set_ID_exist(int(first_input)) == False:
                self.error_list.append(3)
        except:
            self.error_list.append(0)
        
        try:
            int(second_input)
            if sql_functions.is_set_ID_exist(int(second_input)) == False:
                self.error_list.append(4)
        except:
            self.error_list.append(1)
        
        if 0 in self.error_list and 1 in self.error_list:
            self.error_list.remove(0)
            self.error_list.remove(1)
            self.error_list.append(2)
        
        # Should error appear?
        if len(self.error_list) > 0:

            # Error window
            self.popup = ErrorPopup()

            # Error text
            errorText = ""
            for i in self.error_list:
                errorText += Error.error_dict[i] + "\n"

            self.popup.label_error_text.setText(errorText)

            # Show error
            self.popup.exec()
        else:
            pass
        

        
class ErrorPopup(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(gui_path_error, self)

class Error:
    error_dict = {
        0: "First input must be a number.",
        1: "Second input must be a number.",
        2: "Both inputs must be numbers.",
        3: "Your First Set ID was not found.",
        4: "Your Second Set ID was not found."
    }

print(Error.error_dict[0])


class App(QApplication):
    def __init__(self):
        super().__init__()
        self.MainWindow = MainWindow()
        self.ErrorPopup = ErrorPopup()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # error = Error()
    # error.show()

    sys.exit(app.exec())