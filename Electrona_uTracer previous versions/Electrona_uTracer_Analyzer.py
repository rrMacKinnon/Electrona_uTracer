# TODO:  The match-finding algorithms should remove the matched sets from the master dataframe as it computes subsequent
# TODO:  matched sets.  Otherwise, subsequent sets may contain previously paired-tubes and will be invalid.

import pandas as pd
import matplotlib.pyplot as plt
import sys
import time

# Imports the MasterTubeDataFrame file that was pickled from the Electrona_uTracer_Importer program and returns tubes_df
def import_tube_data(filename):

    # Read the MasterTubeDataFrame.pkl file
    tubes_df = pd.read_pickle(filename)

    #Convert all columns containing current measurements to floats
    columns = list(tubes_df.columns.values[3:])
    for i in columns:
        tubes_df[i] = pd.to_numeric(tubes_df[i])
    return tubes_df

# A function to plot every tube's V/I curve in one figure.
def plot_all(tubes_df):
    for row in tubes_df.itertuples():
        plt.plot(row[4:])
    plt.show()

# A function to plot two tubes.  User is prompted to enter two Tube ID numbers.  (No error handling!)
def plot_two_rows(tubes_df):
    first_tube = str(input("Please enter the first Tube ID you'd like to plot:"))
    second_tube = str(input("Please enter the second Tube ID you'd like to plot:"))
    first_tube_data = tubes_df.loc[first_tube]
    plt.plot(first_tube_data[4:])
    second_tube_data = tubes_df.loc[second_tube]
    plt.plot(second_tube_data[4:])
    plt.show()

# A function to plot a range of tubes bu Tube ID.  User is prompted to enter a start and stop Tube ID number. (No error handling!)
def plot_range(tubes_df):
    first_tube = str(input("To plot a range of tubes, enter the first Tube ID number:"))
    last_tube = str(input("Now enter the last Tube ID number in the range:"))
    for i in range(int(first_tube), int(last_tube)):
        temp = tubes_df.loc[str(i)]
        plt.plot(temp[4:])
    plt.show()

# A function to plot any tubes specified in a list.
def plot_matched(tubes_df, match_list):
    for i in match_list:
        temp = tubes_df.loc[str(i)]
        plt.plot(temp[3:16])
    plt.show()

# A function to perform a least-squares linear regression on the tube dataset to find n matches to a Tube ID, as
# specified by the user.  The matched list of tubes is printed to the console and the option to plot them is offered.
def find_match(tubes_df):

    # Ask the user to enter the tube ID for the tube they want matched.
    user_choice = input("Please enter the Tube ID of the tube to be matched:")
    n_matches = input("How many matched tubes would you like?")
    tube_to_match = tubes_df.loc[str(user_choice)]

    bias_list = list(tubes_df)[3:]  # The list of bias voltage columns;  i.e. -50, -46, -42, -38, -etc.
    bias_diff_list = []             # The list of new _diff^2 columns, to hold the difference values from tube_to_match

    # For every bias voltage column in the DataFrame, add a new column with the suffix '_diff^2' after the name.
    for i in bias_list:
        newcolumn = str(i + '_diff^2')
        tubes_df[newcolumn] = tubes_df[i]
        bias_diff_list.append(newcolumn)

    # Compute the square of the difference of each current measurement for every tube, compared to the tube_to_match
    # Put all the data into the appropriate _diff^2 column.
    for i in range(len(bias_diff_list)):
        tubes_df[bias_diff_list[i]] = tubes_df[bias_diff_list[i]].apply(lambda x: abs(x - tube_to_match[i+3])**2)

    # Add a column called squares_sum and compute the sum of all the diff squares on each row
    tubes_df['squares_sum'] = tubes_df[bias_diff_list].sum(axis=1)

    # Sort ascending by squares_sum.
    tubes_df_sorted = tubes_df.sort_values('squares_sum')

    # Print the results
    print("\n\n\nThe %s best matches to Tube ID #%s are:\n" % (n_matches, user_choice))
    match_list_pdseries = tubes_df_sorted['tube_ID']
    match_list = match_list_pdseries.tolist()
    match_list = match_list[0:(int(n_matches)+1)]
    for i in match_list:
        print(i)

    # Ask the user if they'd like to see a plot of the results
    plot_results = input("\nWould you like to see a plot of the results? y/n")
    if plot_results == 'y' or 'Y':
        plot_matched(tubes_df, match_list)
    else:
        print("\n\n\nWell alright then.")
        time.sleep(3)
        print("\n"*20)

def find_best_matched_set(tubes_df):

    # Build a list of all the tubes in the dataframe.
    tube_list = tubes_df['tube_ID'].tolist()

    # Get number of tubes to match
    n_matches = input("How many matched tubes would you like in the set?")

    # Create a list to store the master match list sets
    master_match_list = []

    # Create a dataframe to store the scores of the tube sets by primary tube_ID
    score_df = pd.DataFrame()



    for tube in tube_list:
        temp_df = tubes_df.copy()
        tube_to_match = temp_df.loc[str(str(tube))]
        bias_list = list(temp_df)[3:]  # The list of bias voltage columns;  i.e. -50, -46, -42, -38, -etc.
        bias_diff_list = []            # The list of new _diff^2 columns, to hold the difference values

        # For every bias voltage column in the DataFrame, add a new column with the suffix '_diff^2' after the name.
        for i in bias_list:
            newcolumn = str(i + '_diff^2')
            temp_df[newcolumn] = temp_df[i]
            bias_diff_list.append(newcolumn)

        # Compute the square of the difference of each current measurement for every tube, compared to the tube_to_match
        # Put all the data into the appropriate _diff^2 column.
        for i in range(len(bias_diff_list)):
            temp_df[bias_diff_list[i]] = temp_df[bias_diff_list[i]].apply(lambda x: abs(x - tube_to_match[i+3])**2)

        # Add a column called squares_sum and compute the sum of all the diff squares on each row
        temp_df['squares_sum'] = temp_df[bias_diff_list].sum(axis=1)

        # Sort ascending by squares_sum.
        temp_df_sorted = temp_df.sort_values('squares_sum')

        # Calculate the sum of all the diff squares to be used as an overall score
        tube_set_score = temp_df_sorted['squares_sum'].iloc[0:(int(n_matches)+1)].sum()
        # print("Total least-squares score for the matched tube set:", tube_set_score)
        score_df.set_value(tube, 'tube_id', tube)
        score_df.set_value(tube, 'score', tube_set_score)
        score_df_sorted = score_df.sort_values('score')
    print("\nLeast-Squares Matching Score (lower is better):")
    print(score_df_sorted)


def import_pickle_build_dataframe():
    try:
    # Build the dataframe from the MasterTubeDataFrame.pkl file
        tubes_df = import_tube_data('MasterTubeDataFrame.pkl')
    except FileNotFoundError:
        print("\nPROBLEM")
        print("Couldn't find the tube data file."
              "Make sure to run Electrona_uTracer_Importer.py before this program.".center(79))
        sys.exit()
    return tubes_df



# A function to display the welcome screen thing that lists out the menu options
def greeting():
    tubes_df = import_pickle_build_dataframe()

    print("\n\n")
    print(" ELECTRONAUT'S FANCY TUBE DATA COMPARATOR ".center(79, "*"))
    # print("MENU of OPTIONS".center(79))
    # print(("***************").center(79))
    print("1) Plot all tubes".center(79))
    print("2) Plot a range of tubes".center(79))
    print("3) Plot a pair of tubes".center(79))
    print("4) Find matches to a particular tube".center(79))
    print("5) Find the closest matched set".center(79))
    print("6) EXIT".center(79))
    print("\n\n\n\n")
    print("What would you like to do? ")
    user_choice = input("\n>>>>> ")

    if int(user_choice) == 1:
        plot_all(tubes_df)
    elif int(user_choice) == 2:
        plot_range(tubes_df)
    elif int(user_choice) == 3:
        plot_two_rows(tubes_df)
    elif int(user_choice) == 4:
        find_match(tubes_df)
    elif int(user_choice) == 5:
        find_best_matched_set(tubes_df)
    elif int(user_choice) =y 6:
        print("\n\ntake it easy...\n\n")
        sys.exit()
    else:
        for i in range(20):
            print("\n")
        print("\n\n***** That wasn't one of the options.")
        print("\n\n")
        time.sleep(3)

    for i in range(8):
        print("\n")



def main():

    tubes_df = import_pickle_build_dataframe()

    while True:
        greeting()



# The standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()