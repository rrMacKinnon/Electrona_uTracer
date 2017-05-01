# The importer should process all the uTracer files and result in a list of dictionaries,
# ready to be converted to a Pandas DataFrame

import os   # needed for directory and file interaction
import tkinter
from tkinter import filedialog
import tkinter.simpledialog as simpledialog
import pandas as pd

global tube_type

# Prompt the user to select a folder containing uTracer files, and return a list of all the files with the .utd ext
def choose_folder():
    root = tkinter.Tk()
    root.withdraw()
    root.directory = filedialog.askdirectory(title='Please select a directory containing uTracer files')
    chosen_folder = root.directory
    working_path = chosen_folder
    os.chdir(chosen_folder)
    list_of_tube_data_files_in_dir = []
    for file in os.listdir(chosen_folder):
        if file.endswith(".utd"):
            list_of_tube_data_files_in_dir.append(file)
    return list_of_tube_data_files_in_dir


def ask_tube_type(prompt = 'Please enter the Tube Type:', confirm = 0):
    while True:
        tube_type = simpledialog.askstring('Tube Type:', 'Please enter the tube type\n for this batch of tubes')
        if not confirm:
            return tube_type


def import_tube_data_file(file_to_open):
    while True:
        try:
            with open(file_to_open, 'r') as file:
                file_contents_string = str(file.read())
                file_contents_list = file_contents_string.split()

                #  Extract the data from the file_contents_list and build a dictionary
                x_values = [i for i in file_contents_list[8::2]]
                y_values = [i for i in file_contents_list[9::2]]
                anode_voltage = {'anode_voltage': file_contents_list[6]}
                tube_ID = {'tube_ID': file_to_open[:-4]}
                tube_data_extras = {**tube_ID, **anode_voltage}  # Combine dicts (Python 3.5)
                tube_data_dict = {**tube_data_extras, **(dict(zip(x_values, y_values)))}

        finally:
                return tube_data_dict

def main():
    # Prompt the user to choose a folder, then make a list of all the files in the chosen directory to be processed
    batch_list = choose_folder()

    tube_type = ask_tube_type('', confirm=0)

    # Read and process every file in the batch_list, then add each resulting tube_data_dict to the master_tube_list
    master_tube_list = []
    for tube in batch_list:
        tube_data_dict = import_tube_data_file(tube)
        tube_data_dict.update({'tube_type':tube_type})
        master_tube_list.append(tube_data_dict)


    # Change the current path back to where this script is
    script_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_path)

    # Export the data as a CSV file
    df = pd.DataFrame(master_tube_list)
    df.to_csv('master_tube_list.csv', index=False)



# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()