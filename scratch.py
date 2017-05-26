def find_match(df):

    # Ask the user to enter the tube ID for the tube they want matched.
    user_choice = input("Please enter the Tube ID of the tube to be matched:")
    n_matches = input("How many matched tubes would you like?")
    tube_to_match = df.loc[str(user_choice)]

    bias_list = list(df)[3:]  # The list of bias voltage columns;  i.e. -50, -46, -42, -38, -etc.
    bias_diff_list = []             # The list of new _diff^2 columns, to hold the difference values from tube_to_match

    # For every bias voltage column in the DataFrame, add a new column with the suffix '_diff^2' after the name.
    for i in bias_list:
        newcolumn = str(i + '_diff^2')
        df[newcolumn] = df[i]
        bias_diff_list.append(newcolumn)

    # Compute the square of the difference of each current measurement for every tube, compared to the tube_to_match
    # Put all the data into the appropriate _diff^2 column.
    for i in range(len(bias_diff_list)):
        df[bias_diff_list[i]] = df[bias_diff_list[i]].apply(lambda x: abs(x - tube_to_match[i+3])**2)

    # Add a column called squares_sum and compute the sum of all the diff squares on each row
    df['squares_sum'] = df[bias_diff_list].sum(axis=1)

    # Sort ascending by squares_sum.
    df_sorted = df.sort_values('squares_sum')

    # Print the results
    print("\n\n\nThe %s best matches to Tube ID #%s are:\n" % (n_matches, user_choice))
    match_list_pdseries = df_sorted['tube_ID']
    match_list = match_list_pdseries.tolist()
    match_list = match_list[0:(int(n_matches)+1)]
    for i in match_list:
        print(i)

    # Ask the user if they'd like to see a plot of the results
    plot_results = input("\nWould you like to see a plot of the results? y/n")
    if plot_results == 'y' or 'Y':
        plot_matched(df, match_list)
    else:
        print("\n\n\nWell alright then.")
        time.sleep(3)
        print("\n"*20)