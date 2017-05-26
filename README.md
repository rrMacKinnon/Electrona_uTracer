# Electrona_uTracer

## Description
This project aims to provide the necessary tools to compare any number of vacuum tubes based on measured data, determine which tubes have matching characteristics, and provide visual representations of the match as well as some statistical information of the sample lot overall.

## Using the software
The software consists of an importer module and an analyzer module.  The importer must be run first to process the tube data files and generate a dataframe, then the analyzer can be run.

## Running the Importer
The user must be prepared with a folder containing any number of uTracer .utd files, each containing current measurements from a series of grid bias voltages.  (A sample dataset is included in a directory called 'SampleTubeData".)

When the Electrona_uTracer_Importer_toCSV.py script is executed, a window will appear prompting the user to choose the directory containing the uTracer files. Navigate to the directy, and click the "choose" button.
A new window will appear, asking you to enter the tube type.  Enter the type and click OK.
The program will process all the data files, build a dataframe, and export the data as a CSV file.  The CSV file will be named "master_tube_list.csv", and will be stored in the root folder of the Electrona_uTracer_Importer_toCSV.py script.

## Running the Analyzer
Once the import has successfully created the 'master_tube_list.csv' file, the Analyzer can be executed.  When it runs, it will read the master_tube_list.csv file and rebuild the dataframe.

Once the dataframe has been rebuilt, all the subsequent functions are available and can be executed one-at-a-time in order.
