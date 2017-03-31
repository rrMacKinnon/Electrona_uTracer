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
            print("Not all x_values are the same")
            return False
    print("All tubes have identical X values")
    return True


def dataFrame_list_builder(master_tube_dict):
    df_tube_ID_list = list(master_tube_dict.keys())
    first_tube = master_tube_dict.get(df_tube_ID_list[0])
    column_list = first_tube.x_values

    for tube in enumerate(df_tube_ID_list):
        temp_tube = master_tube_dict.get(tube[1])


# def least_squares(master_tube_dict, ref_tube):
#     tube_list = master_tube_dict.keys()
#     ref_tube = master_tube_dict.get(ref_tube)
#     print(type(ref_tube))
#     ref_tube_y_values = ref_tube.y_values
#     print(ref_tube_y_values)
#
#     return other_tubes
#
# def chooseTube(master_tube_dict):
#     ref_tube = input('Enter the tube number to be matched')
#     if ref_tube in master_tube_dict.keys():
#         print("We're going to match tube", ref_tube, "which has the following values:")
#
#     else:
#         print("There's no tube in the Master Tube Dictionary with that name.")
#     return # least squares lists for every voltage




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

    print("\n", len(key_list), "tubes were added to the Master Tube Dictionary.")

    if check_all_tubes_share_x_values(master_tube_dict) == True:
        dataFrame_list_builder(master_tube_dict)

    # ref_tube = chooseTube(master_tube_dict)
    # least_squares(master_tube_dict, ref_tube)

    # Lookup each tube in the master_tube_dict and print all its values
#    for key in key_list:
#        lookup_tube = master_tube_dict[key]
#        print("Tube number", lookup_tube.tube_ID, "is of type", lookup_tube.tube_type, "with X values", lookup_tube.x_values,
#              "and Y values", lookup_tube.y_values)



# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()




