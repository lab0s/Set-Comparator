from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QMessageBox
from PyQt5 import uic
import sys
from pathlib import Path
import shutil
import multiprocessing

from sql_functions import *
from comparatorApp import *

class Comparator:
    def __init__(self, first_run, second_run):

        self.failed_runs = combine_two_runs(first_run, second_run)

        

        # Create folder on desktop named diffSet with pathlib module
        self.desktop_path = Path.home() / "Desktop"
        self.diffSet_folder = self.desktop_path / f"diffSet_{first_run}_{second_run}"
        self.diffSet_folder.mkdir(exist_ok=True)

        #Create working folder inside diff folder
        self.diffSet_working_folder = self.diffSet_folder / "_working"
        self.diffSet_working_folder.mkdir(exist_ok=True)

        #Creaet txt file for test whcih failed but does not have a overview.html file
        self.other_problem_runs = self.diffSet_folder / "other_problems.txt"

    def get_tables_path(self, runID):
        testID = get_testID_from_runID(runID)
        return fr"T:\TestExamples\R20\test\{testID}\{runID}\Tables"

    def get_diff_working_path(self):
        diff_path = self.desktop_path / self.diffSet_working_folder
        return diff_path

    def run_comparison(self, list_with_two_runs) -> list:
        """
        Input in form:
        [123, 456]
        """

        first_run = list_with_two_runs[0]
        second_run = list_with_two_runs[1]
        test_ID = get_testID_from_runID(first_run)

        first_path = self.get_tables_path(first_run)
        second_path = self.get_tables_path(second_run)

        current_TE_ID = test_ID

        diff_working_path = self.get_diff_working_path() / f"{current_TE_ID}"
        diff_working_path.mkdir(exist_ok=True)

        absolute_tolerance = get_TE_absolute_tolerance(test_ID)
        relative_tolerance = get_TE_relative_tolerance(test_ID)
        compare_abosolute_values = '0'
        ignore_strings = '0'

        # Comparator run
        instance = run_comparator(
            first_path,
            second_path,
            diff_working_path,
            absolute_tolerance,
            relative_tolerance,
            compare_abosolute_values,
            ignore_strings
        )

        if instance != 2:
            # If there is no difference -> delete folder
            shutil.rmtree(diff_working_path)

        if instance == 2:
            # Copy and rename overview to diffSet folder
            overwiev_file = diff_working_path / f'overview.html'

            if overwiev_file.exists():
                overwiev_file.rename(self.diffSet_folder / f"{current_TE_ID}_{first_run}_{second_run}.html")
            else:
                with self.other_problem_runs.open('a') as f:
                    f.write(f"{current_TE_ID}_{first_run}_{second_run}\n")

    def processing_pool(self):
        if __name__ == "__main__":
            # Create a pool of worker processes
            num_processes = multiprocessing.cpu_count()  # Get the number of CPU cores
            pool = multiprocessing.Pool(processes=num_processes)

            # Distribute the workload across the pool of processes
            results = pool.map(self.run_comparison, self.failed_runs)

            # Close the pool of processes
            pool.terminate()
            pool.join()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        app_path = Path(__file__).resolve().parent
        gui_path_main = app_path / "WindowUI.ui"

        uic.loadUi(gui_path_main, self)

        self.pushButton_compare.clicked.connect(self.compare_clicked)
        # self.pushButton_compare.setText("Compare")

        self.checkBox_useGM.toggled.connect(self.check_useGM)


    def compare_clicked(self):
        # self.loading_window = DialogLoading()
        # self.loading_window.show()
        # self.loading_window_popup = DialogLoading()
        # self.loading_window_popup.exec()
        


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
    
    def check_useGM(self):
        if self.checkBox_useGM.isChecked():
            self.lineEdit_second.setText(f"{get_newest_TIMER_Automatic_run()}")


    def create_error_list(self):
        self.first_input = self.lineEdit_first.text()
        self.second_input = self.lineEdit_second.text()

        self.error_list = []
        self.error_list.clear()

        # Create list of errors
        try:
            int(self.first_input)
            if is_set_ID_exist(int(self.first_input)) == False:
                self.error_list.append(3)
        except:
            self.error_list.append(0)
        
        try:
            int(self.second_input)
            if is_set_ID_exist(int(self.second_input)) == False:
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

        app_path = Path(__file__).resolve().parent
        gui_path_error = app_path / "DialogError.ui"

        uic.loadUi(gui_path_error, self)

class DialogLoading(QDialog):
    def __init__(self):
        super().__init__()

        app_path = Path(__file__).resolve().parent
        gui_path_loading = app_path / "DialogLoading.ui"

        uic.loadUi(gui_path_loading, self)

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())



if __name__ == "__main__":
    main()

