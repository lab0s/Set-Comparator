import os
import multiprocessing
from sql_functions import *
from comparatorApp import *

def run_comparison(run_tuple):
    first_run, second_run = run_tuple
    failed_runs = combine_two_runs(first_run, second_run)
    
    for failed_run in failed_runs:
        first_path = get_tables_path(failed_run[0])
        second_path = get_tables_path(failed_run[1])
        diff_path = get_diff_path()
        absolute_tolerance = get_TE_absolute_tolerance(get_testID_from_runID(failed_run[0]))
        relative_tolerance = get_TE_relative_tolerance(get_testID_from_runID(failed_run[0]))
        compare_abosolute_values = '0'
        ignore_strings = '0'

        # Comparator run
        instance = run_comparator(
            first_path,
            second_path,
            diff_path,
            absolute_tolerance,
            relative_tolerance,
            compare_abosolute_values,
            ignore_strings
        )
        if instance == 2:
            print(f"Run {failed_run[0]} and {failed_run[1]} of TE {get_testID_from_runID(failed_run[0])} are different")

def get_tables_path(runID):
    testID = get_testID_from_runID(runID)
    return fr"T:\TestExamples\R20\test\{testID}\{runID}\Tables"

def get_diff_path():
    diff_path = os.path.join(os.path.join(os.environ['USERPROFILE']), r'Desktop\diff')
    return diff_path

if __name__ == "__main__":
    # Define the runs to compare
    first_run = 33254
    second_run = 33301
    run_tuples = [(first_run, second_run)]

    # Create a pool of worker processes
    num_processes = multiprocessing.cpu_count()  # Get the number of CPU cores
    pool = multiprocessing.Pool(processes=num_processes)

    # Distribute the workload across the pool of processes
    pool.map(run_comparison, run_tuples)

    # Close the pool of processes
    pool.close()
    pool.join()
