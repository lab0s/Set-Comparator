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

print(len(os.listdir(Path(diffSet_folder))))