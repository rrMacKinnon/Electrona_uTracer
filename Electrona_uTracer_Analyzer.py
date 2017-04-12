import pandas as pd
import matplotlib.pyplot as plt
import sys
import time

def import_tube_data(filename):

    # Read the MasterTubeDataFrame.pkl file
    tubes_df = pd.read_pickle(filename)

    #Convert all columns containing current measurements to floats
    columns = list(tubes_df.columns.values[3:])
    for i in columns:
        tubes_df[i] = pd.to_numeric(tubes_df[i])
    return tubes_df

def plot_all(tubes_df):
    for row in tubes_df.itertuples():
        plt.plot(row[4:])
    plt.show()

def plot_two_rows(tubes_df):
    first_tube = str(input("Please enter the first Tube ID you'd like to plot:"))
    second_tube = str(input("Please enter the second Tube ID you'd like to plot:"))
    first_tube_data = tubes_df.loc[first_tube]
    plt.plot(first_tube_data[4:])
    second_tube_data = tubes_df.loc[second_tube]
    plt.plot(second_tube_data[4:])
    plt.show()

def plot_range(tubes_df):
    first_tube = str(input("To plot a range of tubes, enter the first Tube ID number:"))
    last_tube = str(input("Now enter the last Tube ID number in the range:"))
    for i in range(int(first_tube), int(last_tube)):
        temp = tubes_df.loc[str(i)]
        plt.plot(temp[4:])
    plt.show()

def plot_matched(tubes_df, match_list):
    for i in match_list:
        temp = tubes_df.loc[str(i)]
        plt.plot(temp[3:16])
    plt.show()

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
    # print(tubes_df_sorted)

    # Print the results
    print("\n\n\nThe %s best matches to Tube ID #%s are:\n" % (n_matches, user_choice))
    match_list_pdseries = tubes_df_sorted['tube_ID']
    match_list = match_list_pdseries.tolist()
    match_list = match_list[0:(int(n_matches)+1)]
    for i in match_list:
        print(i)

    #  Ask the user if they'd like to see a plot of the results?
    plot_results = input("\nWould you like to see a plot of the reuslts? y/n")
    if plot_results == 'y' or 'Y':
        plot_matched(tubes_df, match_list)
    else:
        print("\n\n\nWell alright then.")
        time.sleep(3)
        for i in range(20):
            print("\n")






def greeting(tubes_df):
    print("\n\nELECTRONAUT'S FANCY TUBE DATA COMPARATOR")
    print("\nOPTIONS")
    print("*******")
    print("1)  Plot all tubes")
    print("2)  Plot a range of tubes")
    print("3)  Plot a pair of tubes")
    print("4)  Find matches to a particular tube")
    print("5)  EXIT")

    print("Please enter the number for the option you'd like:")
    user_choice = input("\n>>>>>> ")
    if int(user_choice) == 1:
        plot_all(tubes_df)
    elif int(user_choice) == 2:
        plot_range(tubes_df)
    elif int(user_choice) == 3:
        plot_two_rows(tubes_df)
    elif int(user_choice) == 4:
        find_match(tubes_df)
    elif int(user_choice) == 5:
        print("\n\ntake it easy...\n\n")
        sys.exit()
    else:
        for i in range(20):
            print("\n")
        print("\n\n***** That wasn't one of the options.")
        print("\n\n")
        time.sleep(3)


def main():
    try:
        # Build the dataframe from the MasterTubeDataFrame.pkl file
        tubes_df = import_tube_data('MasterTubeDataFrame.pkl')
    except FileNotFoundError:
        print("\nPROBLEM")
        print("Couldn't find the tube data file."
              "Make sure to run Electrona_uTracer_Importer.py before this program.".center(78))
        sys.exit()


    while True:
        greeting(tubes_df)



# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()