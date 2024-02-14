from pathlib import Path
import os
import shutil
import multiprocessing
import time

from sql_functions import *
from comparatorApp import *

start_time = time.time()

# set_first = 1
# set_second = 2

# first_run = int(input("Enter first execution ID: "))
# second_run = int(input(("Enter second execution ID: ")))

first_run = 33254
second_run = 33301

failed_runs = combine_two_runs(first_run, second_run)
# pprint(failed_runs)


# Create folder on desktop named diffSet with pathlib module
desktop_path = Path.home() / "Desktop"
diffSet_folder = desktop_path / "diffSet"
diffSet_folder.mkdir(exist_ok=True)

#Create working folder inside diff folder
diffSet_working_folder = diffSet_folder / "_working"
diffSet_working_folder.mkdir(exist_ok=True)


def get_tables_path(runID):
    testID = get_testID_from_runID(runID)
    # return f"T:/TestExamples/R20/test/{testID}/{runID}/Tables"
    return fr"T:\TestExamples\R20\test\{testID}\{runID}\Tables"

def get_diff_working_path():
    diff_path = Path.joinpath(desktop_path, "diffSet", "_working")
    return diff_path

# Comparator inputs
for i in range(len(failed_runs)):
    first_run = failed_runs[i][0]
    second_run = failed_runs[i][1]



def run_comparison(list_with_two_runs) -> list:
    """
    Input in form:
    [123, 456]
    """

    first_run = list_with_two_runs[0]
    second_run = list_with_two_runs[1]

    first_path = get_tables_path(first_run)
    second_path = get_tables_path(second_run)

    current_TE_ID = get_testID_from_runID(first_run)

    diff_working_path = get_diff_working_path() / f"{current_TE_ID}"
    diff_working_path.mkdir(exist_ok=True)

    absolute_tolerance = get_TE_absolute_tolerance(get_testID_from_runID(first_run))
    relative_tolerance = get_TE_relative_tolerance(get_testID_from_runID(first_run))
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
        

        overwiev_file = Path.joinpath(diff_working_path, f'overview.html')
        overwiev_file.rename(Path.joinpath(diffSet_folder, fr"{current_TE_ID}_{first_run}_{second_run}.html"))


if __name__ == "__main__":
        # Create a pool of worker processes
        num_processes = multiprocessing.cpu_count()  # Get the number of CPU cores
        pool = multiprocessing.Pool(processes=num_processes)

        # Distribute the workload across the pool of processes
        pool.map(run_comparison, failed_runs)

        # Close the pool of processes
        pool.close()
        pool.join()
        






