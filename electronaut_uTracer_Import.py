import pandas as pd
import numpy as np
import os

chosen_folder = input("Please enter the path to the folder containing the uTracer files: ")       
tube_type = input("\nWhat type of tubes are these? ")

print("\n— — — — — \n")


# Re-write this as a list comprehension:
os.chdir(chosen_folder)
list_of_tube_data_files_in_dir = []
for file in os.listdir(chosen_folder):
    if file.endswith(".utd"):
        list_of_tube_data_files_in_dir.append(file)

print("Data from", len(list_of_tube_data_files_in_dir), "tubes of type", tube_type, "was successfully read.")

batch_list = list_of_tube_data_files_in_dir
master_tube_list = []

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

for tube in batch_list:
    tube_data_dict = import_tube_data_file(tube)
    tube_data_dict.update({'tube_type':tube_type})
    master_tube_list.append(tube_data_dict) 

# Build the dataframe
df = pd.DataFrame(master_tube_list)    

# Make a list of all the columns
cols = df.columns.tolist()

# Make two new lists, separating the voltage values from the other strings.
# Also, convert the voltages to absolute value ints, so they can be numerically sorted 
voltages = []
other_stuff = []
for i in cols:
    if i.startswith('-'):
        i = int(i[1:])
        voltages.append(i)
    else:
        other_stuff.append(i)

# Sort the voltages numerically
voltages.sort()

# Make a new list to hold the voltages and the other_stuff, properly ordered.
cols_sorted = []

# Add the '-' sign back in to all the voltages and convert to strings, now that they're sorted.
voltages_sorted = []
for i in voltages:
    i = '-' + str(i)
    voltages_sorted.append(i)
    
# Re-order the other_stuff to the desired order    
other_stuff[0], other_stuff[1], other_stuff[2] = other_stuff[1], other_stuff[2], other_stuff[0]    

# Stitch the two separate lists together to form the cols_sorted list.
cols_sorted = other_stuff + voltages_sorted  

# Redefine df with the sorted column list
df = df[cols_sorted]

# Change the bias voltage columns names to something friendlier
column_names = [i.replace('-', 'Bias_') for i in cols_sorted]
df.columns = column_names

# Report how many tubes were processed
total_tubes = df.shape[0]
print("A dataframe containing all", total_tubes, "tubes was successfully created.")
