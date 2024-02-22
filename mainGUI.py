from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QMessageBox
from PyQt5 import uic
import sys
import os
from enum import Enum
import sql_functions
from mainApp_GUI_connect import Comparator

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
        self.create_error_list()

        
        # Should error appear?
        if len(self.error_list) > 0:

            # Error window
            self.popup = ErrorPopup()

            # Error text
            errorText = ""
            for i in self.error_list:
                errorText += self.error_dict()[i] + "\n"

            self.popup.label_error_text.setText(errorText)

            # Show error
            self.popup.exec()
            # self.error_list.clear()
        else:
            print("somethign should happen")
            print(self.first_input, self.second_input)
            print(type(self.first_input), type(self.second_input))
            comparator = Comparator(int(self.first_input), int(self.second_input))
            comparator.processing_pool()
    def create_error_list(self):
        self.first_input = self.lineEdit_first.text()
        self.second_input = self.lineEdit_second.text()

        self.error_list = []
        self.error_list.clear()

        # Create list of errors
        try:
            int(self.first_input)
            if sql_functions.is_set_ID_exist(int(self.first_input)) == False:
                self.error_list.append(3)
        except:
            self.error_list.append(0)
        
        try:
            int(self.second_input)
            if sql_functions.is_set_ID_exist(int(self.second_input)) == False:
                self.error_list.append(4)
        except:
            self.error_list.append(1)
        
        if 0 in self.error_list and 1 in self.error_list:
            self.error_list.remove(0)
            self.error_list.remove(1)
            self.error_list.append(2)
        
        # return self.error_list


    def error_dict(self):
        error_dict = {
            0: "First input must be a number.",
            1: "Second input must be a number.",
            2: "Both inputs must be numbers.",
            3: "Your First Set ID was not found.",
            4: "Your Second Set ID was not found."
        }

        return error_dict


class ErrorPopup(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(gui_path_error, self)

# class App(QApplication):
#     def __init__(self):
#         super().__init__()
#         self.MainWindow = MainWindow()
#         self.ErrorPopup = ErrorPopup()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())