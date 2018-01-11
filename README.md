
"Variable-mu" style audio compression amplifiers require well-matched tubes for best performance.  Unlike fixed-mu tubes that can be matched with few or even one data point, variable-mu tubes operate dynamically across a range of values and should ideally match throughout that range, requiring multiple data points to be compared and matched. This project is intended to help compare any number of variable-mu or remote-cutoff vacuum tubes based on data measured using the excellent uTracer curve tracer by Ronald Dekker (http://www.dos4ever.com/uTracer3/uTracer3_pag0.html).

# Electrona_uTracer

## Description
This project consists of an 'importer' module (which imports uTracer files formatted as "blocks" and builds a dataframe) and the Jupyter Notebook file, which provides a crude step-by-step interface to the comparison and plotting functions.

## Status
So far the matching is working splendidly.  I had all kinds of fancy ideas for the plotting, but once I had this functioning and giving me reliable results, I got excited and went back to building tube amplifiers.

## Execution
1) Copy the path to a directory containing tube data files.  (There are samples files in a directory called 'SampleTubeData')

2) Open the Jupyter Notebook called "Electrona_uTracer_OneJupyter.ipynb".  

3) Run the top cell, and paste in the path

4) Enter a tube type (for the samples, the type is '5749'. (Only supports int names right now))

5) Continue running each subsequent cell.  Note that STEP 5 can take quite a long time (minutes) based on the number of tubes.  The results will be a dataframe with n^2 rows, where n is the number of tube data files processed upon import.

