import os

from sql_functions import *
from comparatorApp import *

# set_first = 1
# set_second = 2

first_run = 2091636
second_run = 2095103


def get_tables_path(runID):
    testID = get_testID_from_runID(runID)
    # return f"T:/TestExamples/R20/test/{testID}/{runID}/Tables"
    return fr"T:\TestExamples\R20\test\{testID}\{runID}\Tables"

def get_diff_path():
    diff_path = os.path.join(os.path.join(os.environ['USERPROFILE']), r'Desktop\diff')
    return diff_path

# print(get_path(second_run))

# Comparator inputs
first_path = get_tables_path(first_run)
second_path = get_tables_path(second_run)
diff_path = get_diff_path()
absolute_tolerance = get_TE_absolute_tolerance(get_testID_from_runID(first_run))
relative_tolerance = get_TE_relative_tolerance(get_testID_from_runID(first_run))




print(first_path)
print(second_path)
print(diff_path)
print(absolute_tolerance)
print(relative_tolerance)





