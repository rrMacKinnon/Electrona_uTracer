# Electrona_uTracer
This project aims to provide the necessary tools to compare any number of vacuum tubes based on measured data, determine which tubes have matching characteristics, and provide visual representations of the match as well as some statistical information of the sample lot overall.

To run the software, the user must be prepared with a folder containing any number of uTracer .utd files, each containing current measurements from a series of grid bias voltages.

First, run Electrona_uTracer_Importer_toCSV.py.  A window should appear prompting you to choose the directory containing the uTracer files.
Navigate to the direct, and click the "choose" button.
A new window should appear, asking you to enter the tube type.  Enter the type and click OK.
The program will process the data files, build a dataframe, and export the data as a CSV file in the root folder of the script.  The CSV file will be named "master_tube_list.csv".
