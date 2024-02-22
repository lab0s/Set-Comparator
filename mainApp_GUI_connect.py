from pathlib import Path
import shutil
import multiprocessing

from sql_functions import *
from comparatorApp import *

# set_first = 1
# set_second = 2

# first_run = int(input("Enter first execution ID: "))
# second_run = int(input(("Enter second execution ID: ")))

first_run = 33485
second_run = 33412

class Comparator:
    def __init__(self, first_run, second_run):

        self.failed_runs = combine_two_runs(first_run, second_run)

        # Create folder on desktop named diffSet with pathlib module
        self.desktop_path = Path.home() / "Desktop"
        self.diffSet_folder = self.desktop_path / "diffSet"
        self.diffSet_folder.mkdir(exist_ok=True)

        #Create working folder inside diff folder
        diffSet_working_folder = self.diffSet_folder / "_working"
        diffSet_working_folder.mkdir(exist_ok=True)

        #Creaet txt file for test whcih failed but does not have a overview.html file
        self.other_problem_runs = self.diffSet_folder / "other_problems.txt"

        # self.processing_pool()

    def get_tables_path(self, runID):
        testID = get_testID_from_runID(runID)
        # return f"T:/TestExamples/R20/test/{testID}/{runID}/Tables"
        return fr"T:\TestExamples\R20\test\{testID}\{runID}\Tables"

    def get_diff_working_path(self):
        diff_path = self.desktop_path / "diffSet" / "_working"
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
        # if __name__ == "__main__":
            # Create a pool of worker processes
            num_processes = multiprocessing.cpu_count()  # Get the number of CPU cores
            pool = multiprocessing.Pool(processes=num_processes)

            # Distribute the workload across the pool of processes
            results = pool.map(self.run_comparison, self.failed_runs)

            # Close the pool of processes
            pool.close()
            pool.join()

comparator = Comparator(first_run, second_run)
comparator.processing_pool()