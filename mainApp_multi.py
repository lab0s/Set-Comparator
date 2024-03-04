from pathlib import Path
import shutil
import multiprocessing

from sql_functions import *
from comparatorApp import *

# set_first = 1
# set_second = 2

# first_run = int(input("Enter first execution ID: "))
# second_run = int(input(("Enter second execution ID: ")))


# failed_runs = combine_two_runs(first_run, second_run)
# pprint(failed_runs)



class ComparatorMulti():
    def __init__(self, first_run, second_run):
        self.first_run = first_run
        self.second_run = second_run

        # Create folder on desktop named diffSet with pathlib module
        self.desktop_path = Path.home() / "Desktop"
        diffSet_folder = self.desktop_path / "diffSet"
        diffSet_folder.mkdir(exist_ok=True)

        #Create working folder inside diff folder
        diffSet_working_folder = diffSet_folder / "_working"
        diffSet_working_folder.mkdir(exist_ok=True)

        self.failed_runs = combine_two_runs(self.first_run, self.second_run)


        self.first_run = first_run
        self.second_run = second_run

        self.run_multi()


    @staticmethod
    def get_tables_path(runID):
        testID = get_testID_from_runID(runID)
        # return f"T:/TestExamples/R20/test/{testID}/{runID}/Tables"
        return fr"T:\TestExamples\R20\test\{testID}\{runID}\Tables"

    def get_diff_working_path(self):
        diff_path = self.desktop_path / "diffSet" / "_working"
        return diff_path

    def run_single_comparison(self, list_with_two_runs) -> list:
        """
        Input in form:
        [123, 456]
        """

        self.first_run = list_with_two_runs[0]
        self.second_run = list_with_two_runs[1]
        test_ID = get_testID_from_runID(self.first_run)

        first_path = self.get_tables_path(self.first_run)
        second_path = self.get_tables_path(self.second_run)

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
            overwiev_file.rename(self.diffSet_folder / f"{current_TE_ID}_{self.first_run}_{self.second_run}.html")

    def run_multi(self):
        if __name__ == "__main__":
                # Create a pool of worker processes
                num_processes = multiprocessing.cpu_count()  # Get the number of CPU cores
                pool = multiprocessing.Pool(processes=num_processes)

                print("Keep calm, this may take a while...")

                # Distribute the workload across the pool of processes
                results = pool.map(self.run_single_comparison, self.failed_runs)

                # Close the pool of processes
                pool.close()
                pool.join()

                print('Done, you can close the program.')


compare = ComparatorMulti(33892, 33891)