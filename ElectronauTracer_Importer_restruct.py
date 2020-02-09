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

# For some reason, .describe is requiring .astype(float) in order to show the stats.
df_stats = df.astype(float).describe()
df_stats.loc[:, 'tube_type'] = df_stats.loc[:, 'tube_type'].astype(int)
df_stats.loc[:, 'tube_ID'] = df_stats.loc[:, 'tube_ID'].astype(int)

print("Stastistics calculated.")
print()
print("Starting difference calculations...  (** This can take a while **)")


# STEP 5: Calculate the differences between all tubes

from ipywidgets import FloatProgress
from IPython.display import display
import time

start_time = time.time() 

def build_difference_df(df, df_stats):
    
    # Display a progress bar
    build_diff_progress_bar = FloatProgress(min=0, max=100)
    display(build_diff_progress_bar)
       
    # Make a list of all the columns in the dataframe
    cols = list(df.columns)
    
    # Make a list of just the bias columns (*** Should re-write this as a list comprehension)    
#     bias_list2 = [bias_list2.append(i) for i in cols if i.startswith('Bias_') == True]

    bias_list = []
    for i in cols:
        if i.startswith('Bias_') == True:
            bias_list.append(i)
    
    
    # Make an empty list to hold the calculated values, to be used to build the difference dataframe
    diff_squared_list = []
    
    # Iterate through the index of tubes in the master dataframe to select a reference tube
    for each_ref_tube in df.index:
        
        # Get the next reference tube data, as a series
        ref_tube = df.iloc[each_ref_tube]
        ref_tube_ID = ref_tube.tube_ID

        # Iterate through the index of tubes in the master dataframe to select a match tube
        for each_match_tube in df.index:
            
            # Get the next tube data to be compared, as a series
            match_tube = df.iloc[each_match_tube]
            match_tube_ID = match_tube.tube_ID
            
            # Dictionary container to hold the difference variables for each tube
            temp_dict = {}
            
            # Compute the squares of the differences in each current measurement
            error_sum = 0
            for bias in enumerate(bias_list):
                mismatch = ((float(match_tube.loc[bias[1]]) - float(ref_tube.loc[bias[1]]))**2)
                temp_dict[bias[1]] = mismatch
                error_sum = error_sum + mismatch

            # Add other relevant key/value pairs to the dictionary  
            temp_dict['ref_tube_ID'] = ref_tube_ID
            temp_dict['match_tube_ID'] = match_tube_ID
            temp_dict['error_sum'] = error_sum

            # Append the tube's calculated values to the diff_squared_list
            diff_squared_list.append(temp_dict)
            
            # Update the progress bar
            build_diff_progress_bar.value += 1

    
    # Make an ordered list for the columns of the new difference dataframe
    new_cols_to_add = ['ref_tube_ID', 'match_tube_ID', 'error_sum']
    df_dif_cols = new_cols_to_add + bias_list
    df_dif = pd.DataFrame(diff_squared_list, columns = df_dif_cols)

    return df_dif
    
    
df_dif = build_difference_df(df, df_stats)

# Produce a brief report:
total_rows = len(df_dif)
total_columns = len(df_dif.columns)
total_datapoints = total_rows * total_columns
stop_time = time.time()
elapsed_time = stop_time - start_time
print("It took", round(elapsed_time, 2), "seconds to calculate", 
      total_datapoints, "values, resulting in", len(df_dif), "rows.")

# Display the head of the difference dataframe
# df_dif.head()

# Plot a line graph of all tubes

from bokeh.plotting import figure, output_file, show

output_file("Tube_Batch_Statistics.html")

# Configure the size, title, etc.
p = figure(plot_width=1000, plot_height=750, title="Plate Current as a function of Grid Voltage")
p.title.text_color = "black"

# Make a list for the x_values by chopping off all the "bias_" column name prefixes and converting to ints
temp_columns = list(df_stats.columns)
stats_columns = []
x_values = [int(i[5:]) for i in temp_columns if i.startswith('Bias_') == True]        

# Add all rows of tubes
for i in range(len(df.index)):
    row = df.iloc[i]
    row = list(row)
    row = row[3:]
    p.line(x_values, row, line_width=2)

# Set axis labels
p.xaxis.axis_label = "Grid Voltage (V)"
p.xaxis.axis_label_text_color = "#aa6666"
p.yaxis.axis_label = "Plate Current (mA)"

# Set grid lines
p.ygrid.minor_grid_line_color = 'navy'
p.ygrid.minor_grid_line_alpha = 0.2
p.xgrid.minor_grid_line_color = 'navy'
p.xgrid.minor_grid_line_alpha = 0.2

# Set background color
p.background_fill_color = "beige"
p.background_fill_alpha = 0.5

# Show the plot
show(p)



# This function requires the tube_to_match and tube_set_size variable to be set manually, below.

def find_best_set_for_chosen_tube_ID():
    
    tube_to_match = input("What tube number would you like to match? ")
    tube_set_size = int(input("How many matches would you like? ")) + 1
    
    # Create a new dataframe showing only tube_set_size number of nearest matches to the chosen tube_to_match
    df_tube_set = df_dif[(df_dif.ref_tube_ID == str(tube_to_match))].sort_values('error_sum').head(tube_set_size)
    
    return df_tube_set