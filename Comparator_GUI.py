from sys import stdout
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import os
import subprocess
import webbrowser

# Desktop path for later use
desktop_path = Path.home() / "Desktop"

# Path to TortoiseGitMerge.exe
# Check existence of TortoiseGitMerge.exe in different Program Files directories
if os.path.exists(os.path.join(os.environ.get('ProgramFiles', ''), 'TortoiseGit', 'bin', 'TortoiseGitMerge.exe')):
    rx_tortoise = os.path.join(os.environ['ProgramFiles'], 'TortoiseGit', 'bin', 'TortoiseGitMerge.exe')
elif os.path.exists(os.path.join(os.environ.get('ProgramFiles(x86)', ''), 'TortoiseGit', 'bin', 'TortoiseGitMerge.exe')):
    rx_tortoise = os.path.join(os.environ['ProgramFiles(x86)'], 'TortoiseGit', 'bin', 'TortoiseGitMerge.exe')
elif os.path.exists(os.path.join(os.environ.get('ProgramW6432', ''), 'TortoiseGit', 'bin', 'TortoiseGitMerge.exe')):
    rx_tortoise = os.path.join(os.environ['ProgramW6432'], 'TortoiseGit', 'bin', 'TortoiseGitMerge.exe')
else:
    rx_tortoise = None  # If TortoiseGitMerge.exe is not found in any expected location




file_path = os.path.abspath(os.path.dirname(__file__))



# Main app
class MainApplication(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Strings to argument
        self.first_path_by_path = ''
        self.first_path_by_ID = ''
        self.second_path_by_path = ''
        self.second_path_by_ID = ''
        self.diff_path = ''
        self.absolute_tolerance = ''
        self.relative_tolerance = ''
        self.compare_absolute_values = ''
        self.ignore_strings = ''

        # Set default diff_path as desktop/diff path
        self.diff_path = os.path.join(os.path.join(os.environ['USERPROFILE']), r'Desktop\diff')

        # row counter
        row = 0

        # frm_manual
        self.frm_manual_main = frm_manual(self)
        self.frm_manual_main.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # frm_column_name
        self.frm_column_name_main = frm_column_name(self)
        self.frm_column_name_main.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # frm_first_path_by_ID
        self.frm_first_ID_main = frm_test_id(self, 'First run by ID:', 2, 3)
        self.frm_first_ID_main.frm_test_name_label.focus_force()
        self.frm_first_ID_main.grid(row=row, column=0, sticky='SNEW')
        row += 1


        # Initialize radio_var_first
        self.radio_val_first = ''
        self.radio_var_first = tk.StringVar()

        self.frm_first_ID_main.frm_test_name_radioButton['variable'] = self.radio_var_first
        self.frm_first_ID_main.frm_test_name_radioButton.config(command=lambda: get_selection())

        self.frm_first_ID_main.frm_run_id_entry.bind("<FocusIn>", lambda event: entry_focus_in(event, 'first'))
        self.frm_first_ID_main.frm_run_id_entry.bind("<FocusOut>", lambda event: entry_focus_out_get_first(event))

        # frm_first_path
        self.frm_first_path_main = frm_folder_path(self, 'First run by path:', 2, 3)
        self.frm_first_path_main.grid(row=row, column=0, sticky='SNEW')
        row += 1

        self.frm_first_path_main.frm_folder_path_radioButton['variable'] = self.radio_var_first
        self.frm_first_path_main.frm_folder_path_radioButton.config(command=lambda: get_selection())

        self.frm_first_path_main.frm_path_button.configure(command=lambda: set_path("first"))

        # set default value for radio button to be checked
        self.radio_var_first.set("First run by ID:")


        # fill
        self.frm_fill_2 = frm_fill(self)
        self.frm_fill_2.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # frm_second_path_by_ID
        self.frm_second_ID_main = frm_test_id(self, 'Second run by ID:', 2, 3)
        self.frm_second_ID_main.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # Initialize radio_val_second
        self.radio_val_second = ''
        self.radio_var_second = tk.StringVar()

        self.frm_second_ID_main.frm_test_name_radioButton['variable'] = self.radio_var_second
        self.frm_second_ID_main.frm_test_name_radioButton.config(command=lambda: get_selection())

        self.frm_second_ID_main.frm_run_id_entry.bind("<FocusIn>", lambda event: entry_focus_in(event, 'second'))
        self.frm_second_ID_main.frm_run_id_entry.bind("<FocusOut>", lambda event: entry_focus_out_get_second(event))
        
        # frm_second_path
        self.frm_second_path_main = frm_folder_path(self, 'Second run by path:', 2, 3)
        self.frm_second_path_main.grid(row=row, column=0, sticky='SNEW')
        row += 1

        self.frm_second_path_main.frm_folder_path_radioButton['variable'] = self.radio_var_second
        self.frm_second_path_main.frm_folder_path_radioButton.configure(command=lambda: get_selection())

        self.frm_second_path_main.frm_path_button.configure(command=lambda: set_path("second"))

        # set default value for radio button to be checked
        self.radio_var_second.set("Second run by ID:")


        # fill
        self.frm_fill_2 = frm_fill(self)
        self.frm_fill_2.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # frm_diff_folder
        self.frm_diff_folder_main = frm_diff_folder_path(self, 'Diff Folder:', 2, 3)
        self.frm_diff_folder_main.grid(row=row, column=0, sticky='SNEW')
        self.frm_diff_folder_main.frm_path_label_show['text'] = f"{self.diff_path}" # bude pouzito jako default v pripade ze uzivatel nezvoli jinou cestu
        row += 1

        self.frm_diff_folder_main.frm_path_button.configure(command=lambda: set_path("diff"))

        # fill
        self.frm_fill_1 = frm_fill(self)
        self.frm_fill_1.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # frm_aboslute_tolerance
        self.frm_absolute_tolerance_main = frm_tolerance(self, 'Absolute Tolerance [-]', 2)
        self.frm_absolute_tolerance_main.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # frm_relative_tolerance
        self.frm_relative_tolerance_main = frm_tolerance(self, 'Relative Tolerance [%]', 2)
        self.frm_relative_tolerance_main.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # fill
        self.frm_fill_2 = frm_fill(self)
        self.frm_fill_2.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # frm_compare_absolute_values
        self.frm_compare_absolute_values_main = frm_checkbox(self, 'Compare Absolute Values')
        self.frm_compare_absolute_values_main.grid(row=row, column=0, sticky='SNEW')
        self.frm_absolute_tolerance_main.frm_tolerance_entry.insert(0, 0.002) # default value
        row += 1

        # frm_ignore_strings
        self.frm_ignore_strings_main = frm_checkbox(self, 'Ignore Strings')
        self.frm_ignore_strings_main.grid(row=row, column=0, sticky='SNEW')
        self.frm_relative_tolerance_main.frm_tolerance_entry.insert(0, 1) # default value
        row += 1

        # fill
        self.frm_fill_2 = frm_fill(self)
        self.frm_fill_2.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # frm_informations
        self.frm_informations_main = frm_infromations(self)
        self.frm_informations_main.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # fill
        self.frm_fill_2 = frm_fill(self)
        self.frm_fill_2.grid(row=row, column=0, sticky='SNEW')
        row += 1

        # frm_bottom_buttons
        self.frm_bottom_buttons_main = frm_bottom_buttons(self)
        self.frm_bottom_buttons_main.grid(row=row, column=0, sticky='SW')
        row += 1

        self.frm_bottom_buttons_main.compare_button.configure(command=lambda: compare())
        self.frm_bottom_buttons_main.overview_button.configure(command=lambda: show_overview(), state='disabled')
        self.frm_bottom_buttons_main.compare_xml_button.configure(command=lambda: compare_xml(), state='disabled')


        # final setup
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


        # Function to handle the Entry widget focus events
        def entry_focus_out_get_first(event):
            runID = self.frm_first_ID_main.frm_run_id_entry.get()
            runID = str(runID).replace(" ", "")
            testID = find_testID(self, test_dict, runID)
            self.frm_first_ID_main.frm_test_id_label['text'] = testID
            self.first_path_by_ID = f"T:/TestExamples/R20/test/{testID}/{runID}/Tables"
            show_xml_comparison()
            # print(self.first_path_by_ID)

        def entry_focus_out_get_second(event):
            runID = self.frm_second_ID_main.frm_run_id_entry.get()
            runID = str(runID).replace(" ", "")
            testID = find_testID(self, test_dict, runID)
            self.frm_second_ID_main.frm_test_id_label['text'] = testID
            self.second_path_by_ID = f"T:/TestExamples/R20/test/{testID}/{runID}/Tables"
            show_xml_comparison()
            # print(self.second_path_by_ID)
        
        
        def find_testID(self, dictionary, value):
            for key, lst in dictionary.items():
                if value in lst:
                    return key
            return 'TE not found'  # Return None if the value is not found in any list



        # Set buttons for test setup and paths
        def set_path(text):
            # Set default Information text when new paths are set
            setDefaultInformationText(self)

            if text == "first":
                self.radio_var_first.set("First run by path:")
                dir = filedialog.askdirectory(initialdir=desktop_path)
                self.frm_first_path_main.frm_path_label_show['text'] = f"{dir}"
                self.first_path_by_path = f"{dir}"
            if text == "second":
                self.radio_var_second.set("Second run by path:")
                dir = filedialog.askdirectory(initialdir=desktop_path)
                self.frm_second_path_main.frm_path_label_show['text'] = f"{dir}"
                self.second_path_by_path = f"{dir}"
            if text == "diff":
                dir = filedialog.askdirectory(initialdir=desktop_path)
                self.frm_diff_folder_main.frm_path_label_show['text'] = f"{dir}"

                self.frm_diff_folder_main.frm_path_label_show['text'] = ''
                self.frm_diff_folder_main.frm_path_label_show['text'] = dir
                self.diff_path = dir
        

        def set_tolerance():
            self.absolute_tolerance = float(str(self.frm_absolute_tolerance_main.frm_tolerance_entry.get()).replace(",", "."))
            self.relative_tolerance = float(str(self.frm_relative_tolerance_main.frm_tolerance_entry.get()).replace(",", ".")) #/ 100 # divided by 100 to get value without percent

        def set_checkbox():
            self.compare_absolute_values = self.frm_compare_absolute_values_main.check_var.get()
            self.ignore_strings = self.frm_ignore_strings_main.check_var.get()
        
        def get_first_path():
            if self.radio_var_first.get() == "First run by ID:":
                return self.first_path_by_ID
            elif self.radio_var_first.get() == "First run by path:":
                return self.first_path_by_path
        
        def get_second_path():
            if self.radio_var_second.get() == "Second run by ID:":
                return self.second_path_by_ID
            elif self.radio_var_second.get() == "Second run by path:":
                return self.second_path_by_path

        def get_comparator_output():
            process = subprocess.Popen([
                comparator_path, 
                f"{get_first_path()}", 
                f"{get_second_path()}", 
                f"{self.diff_path}", 
                f"{self.absolute_tolerance}", 
                f"{self.relative_tolerance}", 
                f"{self.compare_absolute_values}", 
                f"{self.ignore_strings}"],
                stdout=subprocess.PIPE)
            
            process.wait()
            output = process.returncode
            process.terminate()
            
            # print(output)

            if output == 0:
                self.frm_informations_main.frm_manual_text_label['text'] = f"Informations / warnings:\nNo difference found."
            elif output == 1:
                self.frm_informations_main.frm_manual_text_label['text'] = f"Informations / warnings:\nYou entered incorrect parameters."
            elif output == 2:
                self.frm_informations_main.frm_manual_text_label['text'] = f"Informations / warnings:\nDifference found."
            else:
                self.frm_informations_main.frm_manual_text_label['text'] = f"Informations / warnings:\nDiff cannot be done or missing data."
