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
    first_tube = str(input("Please enter the index of the first tube you'd like to plot:"))
    second_tube = str(input("Please enter the index of the second tube you'd like to plot:"))
    first_tube_data = tubes_df.loc[first_tube]
    plt.plot(first_tube_data[4:])
    second_tube_data = tubes_df.loc[second_tube]
    plt.plot(second_tube_data[4:])
    plt.show()    #Convert all columns containing current measurements to floats
    for i in columns:
        tubes_df[i] = pd.to_numeric(tubes_df[i])


def plot_range(tubes_df):
    first_tube = str(input("To plot a range of tubes, enter the first Tube ID number:"))
    last_tube = str(input("Now enter the last Tube ID number in the range:"))
    for i in range(int(first_tube), int(last_tube)):
        temp = tubes_df.loc[str(i)]
        plt.plot(temp[4:])
    plt.show()

def find_match(tubes_df):

    # Ask the user which tube should be matched
    user_choice = input("Please enter the tube number to match:")
    tube_to_match = tubes_df.loc[str(user_choice)]
    # print("Tube to Match:", tube_to_match)
    # print("Tubes_DF", tubes_df)

    # Add a new column with the suffix '_diff^2' to each bias voltage column and fill with zeros
    bias_list = list(tubes_df)[3:]
    for i in bias_list:
        newcolumn = str(i + '_diff^2')
        tubes_df[newcolumn] = tubes_df[i]


    print("Tube to match:", tube_to_match[4])

    tweak_list = list(tubes_df)[16:]
    # print("Tweak List:", tweak_list)


    #  Sample compute squares:  works on a static line.  Need to loop this through the dataframe
    tubes_df[tweak_list[0]] = tubes_df[tweak_list[0]].apply(lambda x: abs(x - tube_to_match[3])**2)

    print("\nThis is a column of the difference squares of -50 relative to the ref tube:\n", tubes_df[tweak_list[0]])



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
    user_choice = int(input("\n>>>>>> "))
    if user_choice == 1:
        plot_all(tubes_df)
    elif user_choice == 2:
        plot_range(tubes_df)
    elif user_choice == 3:
        plot_two_rows(tubes_df)
    elif user_choice == 4:
        find_match(tubes_df)
    elif user_choice == 5:
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
        print("Couldn't find the tube data file.  Make sure to run Electrona_uTracer_Importer.py before this program.".center(78))
        sys.exit()


    while True:
        greeting(tubes_df)



# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()