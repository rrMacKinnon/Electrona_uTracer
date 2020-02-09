

# STEP 7:  Build a dataframe of the best matched sets in order

# math lib used for generating ordinal strings; i.e. ['1st', '2nd', '3rd'] etc.
import math

# Make a local version of df_dif that can be butchered
df_dif_copy = df_dif.copy()

def ask_tube_set_size():
    
    # Ask the user to enter the set size
    tube_set_size = input("Please enter the number of tubes per matched set:")
    
    # Build a list of tube names for the tube set size
    tube_sets_columns = ['Tube_' + str(1 + i) for i in range(int(tube_set_size))]    
    
    return tube_set_size, tube_sets_columns 


def find_best_set_for_chosen_tube_ID(df_dif_copy, tube_to_match, tube_set_size, tube_sets_columns):
    tube_to_match = str(tube_to_match)
        
    # Create a new dataframe showing only tube_set_size number of nearest matches to the chosen tube_to_match
    df_tube_set = df_dif_copy[(df_dif_copy.ref_tube_ID == tube_to_match)].sort_values('error_sum').head(int(tube_set_size))
        
    # Create the dictionary of the tubes in the set and the total score of the set
    tube_set_list = list(df_tube_set.match_tube_ID)
    tube_set_dict = dict(zip(tube_sets_columns, tube_set_list))   
    tube_set_score = df_tube_set.error_sum.sum()
    tube_set_dict.update({'tube_set_score':tube_set_score})

    return tube_set_dict


def find_best_set(df_dif_copy, tube_set_size, tube_sets_columns):
    
    # Make an empty list to hold the tube sets and their scores
    tube_sets_and_scores_list = []
    temp_dict = {}
    
    if 'tube_set_score' in tube_sets_columns:
        tube_sets_columns.remove('tube_set_score')

    for i in df_dif_copy.ref_tube_ID.unique():
        temp_dict = find_best_set_for_chosen_tube_ID(df_dif_copy, i, tube_set_size, tube_sets_columns)
        tube_sets_and_scores_list.append(temp_dict)

    # Add 'tube_set_score' column name at the front of the list
    if 'tube_set_score' not in tube_sets_columns: 
        tube_sets_columns.insert(0, 'tube_set_score')    
    
    # Create a dataframe for the tube sets called df_tube_sets 
    df_tube_sets = pd.DataFrame(tube_sets_and_scores_list, columns=tube_sets_columns)
    
    # Sort the tube_set_score column, take the top row (with the lowest score) as a new df 
    df_best_set_temp = df_tube_sets.sort_values('tube_set_score').head(1)
        
    return df_best_set_temp


# A function to plot a line graph of a set of tubes by passing in a list of tube numbers
def plot_tubes(list_of_tubes, df):
    
    output_file("Tube_Set_Statistics.html")

    # Configure the size, title, etc.
    p = figure(plot_width=1000, plot_height=750, title=str(list_of_tubes))
    p.title.text_color = "black"

    # Make a list for the x_values by chopping off all the "bias_" column name prefixes and converting to ints
    temp_columns = list(df.columns)
    x_values = [int(i[5:]) for i in temp_columns if i.startswith('Bias_') == True]        


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

    for tube in list_of_tubes:
        row = ((df.loc[df['tube_ID'] == tube[0:3]]).values.tolist())[0]
        row = [float(i) for i in row[3:]]
        p.line(x_values, row, line_width=2)

    return p    


    
# Start a timer
start_time = time.time()   
    
# Make an empty dataframe to hold all the sets and their scores
df_best_tube_sets = pd.DataFrame()

# Get the tube_set_size and the tube_sets_columns from the ask_tube_set_size function
tube_set_size, tube_sets_columns = ask_tube_set_size()

# Get the best tube set from the batch
df_best_set_temp = find_best_set(df_dif_copy, tube_set_size, tube_sets_columns) 

# Display a progress bar
progress_bar_range = int(len(df)/int(tube_set_size))
best_matched_progress_bar = FloatProgress(min=0, max=progress_bar_range)
display(best_matched_progress_bar)

# Append the best tube set to the df_best_tube_sets dataframe
df_best_tube_sets = df_best_tube_sets.append(df_best_set_temp)

# Remove the best tube set from df_dif_copy
tube_delete_list = list(df_best_set_temp.iloc[0])
tube_delete_list.pop(0)
df_dif_copy = df_dif_copy[~df_dif_copy.ref_tube_ID.isin(tube_delete_list)]
df_dif_copy = df_dif_copy[~df_dif_copy.match_tube_ID.isin(tube_delete_list)]

# A function to generate ordinal strings; i.e. ['1st', '2nd', '3rd'] etc.
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
ordinal_list = [ordinal(n) for n in range(1, int(len(df)))]

set_count = 1
print()
print("*** BEST! ***")
print(ordinal_list[0],"best tube set SCORE:", str(df_best_set_temp.tube_set_score.iloc[0]))
print("TUBES:", tube_delete_list)

# Update the progress bar
best_matched_progress_bar.value += 1

tube_matches_master_plot_list = []

while len(df_dif_copy.ref_tube_ID.unique()) >= int(tube_set_size):

    # Get all the rest of the sets from the batch
    df_best_set_temp = find_best_set(df_dif_copy, tube_set_size, tube_sets_columns)
    
    # Append the best tube set to the df_best_tube_sets dataframe
    df_best_tube_sets = df_best_tube_sets.append(df_best_set_temp)

    # Remove the best tube set from df_dif_copy
    tube_delete_list = list(df_best_set_temp.iloc[0])
    tube_delete_list.pop(0)

    df_dif_copy = df_dif_copy[~df_dif_copy.ref_tube_ID.isin(tube_delete_list)]
    df_dif_copy = df_dif_copy[~df_dif_copy.match_tube_ID.isin(tube_delete_list)]
    print()
    print(ordinal_list[set_count],"best tube set SCORE:", str(df_best_set_temp.tube_set_score.iloc[0]))
    print("TUBES:", tube_delete_list)
    tube_delete_list.insert(0, ordinal)

    tube_matches_master_plot_list.insert(1 ,tube_delete_list[1:])

    set_count += 1
    
    # Update the progress bar
    best_matched_progress_bar.value += 1

    
    



stop_time = time.time()
elapsed_time = stop_time - start_time
print()
print("It took", round(elapsed_time, 2), "seconds to produce", set_count, "tube sets.")

# print(tube_matches_master_plot_list[0])

# plot_tubes((list(df_best_tube_sets.iloc[0])[1:]), df)
    
# Build the plot object
# tube_plot = plot_tubes(tube_delete_list, df)

# Show the plot
# show(tube_plot)



best_set_list = list(df_best_tube_sets.iloc[0])[1:]
worst_set = df_best_tube_sets.tail(1)
worst_set_list = list(worst_set.iloc[0])[1:]



