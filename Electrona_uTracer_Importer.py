#  This program reads and processes the text files produced by the uTracer, resulting in a master_tube_dict containing
#  tube objects which each contain voltages, currents, and related attributes.

import os   # needed for directory and file interaction
import tkinter
from tkinter import filedialog
import tkinter.simpledialog as simpledialog
import pandas as pd

global tube_type

class Tube:

    def __init__(self, tube_ID, x_values, y_values, anode_voltage, tube_type='5749'):
        self.tube_ID = tube_ID
        self.x_values = x_values
        self.y_values = y_values
        self.anode_voltage = anode_voltage
        self.tube_type = tube_type

# Prompt the user to select a folder containing uTracer files, and return a list of all the files with the .utd ext
def choose_folder():
    root = tkinter.Tk()
    root.withdraw()
    root.directory = filedialog.askdirectory(title='Please select a directory containing uTracer files')
    chosen_folder = root.directory
    os.chdir(chosen_folder)
    print("\n")
    print("chosen_folder:", chosen_folder)
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


# This function takes a filename argument, looks for that file in the current directory, reads it into a string,
# then generates lists and variables which are passed as arguments during Tube class instantiation.
def import_tube_data_file(file_to_open):
    while True:
        try:
            with open(file_to_open, 'r') as file:
                file_contents_string = str(file.read())
                file_contents_list = file_contents_string.split()
                x_values = [i for i in file_contents_list[8::2]]
                y_values = [i for i in file_contents_list[9::2]]
                anode_voltage = file_contents_list[6]
                tube_ID = file_to_open[:-4]
                tube_object = Tube(tube_ID, x_values, y_values, anode_voltage)
        finally:
                return tube_object


# Compares every value in the x_values list of each tube to the values in the first tube to make sure they're identical.
def check_all_tubes_share_x_values(dict):
    tube_list = list(dict.keys())
    ref_tube = dict.get(tube_list[0])
    ref_x_values = list(ref_tube.x_values)
    for tube in tube_list:
        temp_tube = dict.get(tube)
        if temp_tube.x_values != ref_x_values:
            return False
        else:
            len_of_x_values = len(ref_x_values)
            print("All tubes have", len_of_x_values, "identical X values.")
            return True


def dataFrame_list_builder(master_tube_dict):
    master_tubeID_list = list(master_tube_dict.keys())
    first_tube = master_tube_dict.get(master_tubeID_list[0])
    tube_object_attribute_list = list((vars(first_tube)).keys())

    # build a list of column names
    column_list = []
    column_list = column_list + first_tube.x_values
    column_list.insert(0, tube_object_attribute_list[0])  # Insert Tube_ID to the front of the column list
    column_list.insert(1, tube_object_attribute_list[-1]) # Insert tube-type into position 1 in the column list
    column_list.insert(2, tube_object_attribute_list[3])  # Insert anode_voltage into position 2 of the column list

    # Create empty dataframe with columns assigned
    tubes_df = pd.DataFrame(columns=column_list, index=[master_tubeID_list])

    # Loop through the tube list and add each tube's values to the dataframe
    for tube in master_tubeID_list:
        temp_tube = master_tube_dict.get(tube)
        temp_tube_dict = {}
        temp_tube_dict.update({'tube_ID':temp_tube.tube_ID})
        temp_tube_dict.update({'anode_voltage':temp_tube.anode_voltage})
        temp_tube_dict.update({'tube_type':temp_tube.tube_type})
        temp_tube_dict.update(dict(zip(temp_tube.x_values,temp_tube.y_values)))
        tubes_df.loc[tube] = pd.Series(temp_tube_dict)
    return tubes_df


def main():
    #  master_tube_dict is a dictionary for storing all the Tube objects
    master_tube_dict = {}

    # Prompt the user to choose a folder, then make a list of all the files in the chosen directory to be processed
    batch_list = choose_folder()

    tube_type = ask_tube_type('', confirm=0)

    # Read and process every file in the batch_list, then add each resulting Tube object to the master_tube_dict
    for tube in batch_list:
        tube_object = import_tube_data_file(tube)
        tube_object.tube_type = tube_type
        master_tube_dict.update({tube_object.tube_ID: tube_object})

    # Print the number of tube objects that were created
    key_list = master_tube_dict.keys()

    print(len(key_list), "tubes were processed and added to the Master Tube Dictionary.")

    if check_all_tubes_share_x_values(master_tube_dict) == False:
        print("Processing failed because not all times have the same X values.")

    print("\n")
    tubes_df = dataFrame_list_builder(master_tube_dict)
    print(tubes_df)



# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()




