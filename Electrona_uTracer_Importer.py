#  This program reads and processes the text files produced by the uTracer, resulting in a master_tube_dict containing
#  tube objects which each contain voltages, currents, and related attributes.

import os   # needed for directory and file interaction
import tkinter
from tkinter import filedialog


class Tube:

    def __init__(self, tube_ID, x_values, y_values, anode_voltage):
        self.tube_ID = tube_ID
        self.x_values = x_values
        self.y_values = y_values
        self.anode_voltage = anode_voltage


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

def main():
    #  master_tube_dict is a dictionary for storing all the Tube objects
    master_tube_dict = {}

    # Prompt the user to choose a folder, then make a list of all the files in the chosen directory to be processed
    batch_list = choose_folder()

    # Read and process every file in the batch_list, then add each one to the master_tube_dict
    for tube in batch_list:
        tube_object = import_tube_data_file(tube)
        master_tube_dict.update({tube_object.tube_ID: tube_object})

    # Print the number of tube objects that were created
    key_list = master_tube_dict.keys()
    print("\n", len(key_list), "tubes were added to the Master Tube Dictionary.")

    # Lookup each tube in the master_tube_dict and print all its values
    for key in key_list:
        lookup_tube = master_tube_dict[key]
        print("Tube number", lookup_tube.tube_ID, "with X values", lookup_tube.x_values,
              "and Y values", lookup_tube.y_values)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()




