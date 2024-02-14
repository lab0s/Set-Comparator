import os
import pathlib
import shutil
import multiprocessing

from sql_functions import *
from comparatorApp import *




# Create folder on desktop named diffSet with pathlib module
desktop_path = pathlib.Path.home() / "Desktop"
diffSet_folder = desktop_path / "diffSet"
diffSet_folder.mkdir(exist_ok=True)

#Create working folder inside diff folder
diffSet_working_folder = diffSet_folder / "working"
diffSet_working_folder.mkdir(exist_ok=True)

def move_folder(original_path, new_path):
    """
    Move folder with files inside it to new location
    """

    # Current folder
    original = pathlib.Path(original_path)


    # Create new folder
    new = pathlib.Path.mkdir(new_path, exist_ok=True)

    # print(list(original_path.iterdir()))

# move_folder()

# print(list(pathlib.Path(r'C:\Users\KovarJ\Desktop\diffSet\working\1885').iterdir()))

move_folder(diffSet_working_folder, diffSet_folder / "12345")
    

    







    