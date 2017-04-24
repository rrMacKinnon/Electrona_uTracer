#  Read tube data files and dynamically build dataframes for each voltage and current, regardless of the number
#  of datapoints.

import os
import pandas as pd


# Prompt the user to select a folder containing uTracer files, and return a list of all the files with the .utd ext
chosen_folder = "/Users/robroy/Desktop/Electrona_uTracer/Electrona_uTracer/SampleTubeData"
working_path = chosen_folder
os.chdir(chosen_folder)
print("\n")
print("chosen_folder:", chosen_folder)

list_of_tube_data_files_in_dir = []

for file in os.listdir(chosen_folder):
    if file.endswith(".utd"):
        list_of_tube_data_files_in_dir.append(file)

print(list_of_tube_data_files_in_dir)

# Select the first file in the list for testing
file_to_open = list_of_tube_data_files_in_dir[0]

# # This function takes a filename argument, looks for that file in the current directory, reads it into a string,
# # then generates lists and variables which are passed as a dictionary to a dataframe.
def import_tube_data_file(file_to_open):
    while True:
        try:
            with open(file_to_open, 'r') as file:
                file_contents_string = str(file.read())
                file_contents_list = file_contents_string.split()

                #  Extract the data from the file_contents_list and assign to variables
                x_values = [i for i in file_contents_list[8::2]]
                y_values = [i for i in file_contents_list[9::2]]
                anode_voltage = file_contents_list[6]
                tube_ID = file_to_open[:-4]

                #  Build a dictionary with key/value pairs to be used when adding rows to the dataframe
                tube_data_dict_list = [{'tube_ID': tube_ID},
                    {'anode_voltage': anode_voltage}]
                tube_data_dict_list.append(dict(zip(x_values, y_values)))

        finally:
                return tube_data_dict_list





tube_data_dict_list = import_tube_data_file(file_to_open)
print("Tube Data Dict List:", tube_data_dict_list)


tubes_df = pd.DataFrame(tube_data_dict_list)
print(tubes_df)




# # This is the standard boilerplate that calls the main() function.
# if __name__ == '__main__':
#   main()