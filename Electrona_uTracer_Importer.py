#  This program should be able to read and process the text files produced by the uTracer.
#  The result should be a tube object for each tube serial number containing all the measurement data
#  additional attributes can be added as ideas come up:  timestamp, etc.

import os   # needed for directory and file interaction
import tkinter
from  tkinter import filedialog


# Prompt the user to select a folder containing uTracer files
def chooseFolder():

    root = tkinter.Tk()
    root.withdraw()
    root.directory = filedialog.askdirectory(title='Please select a directory containing uTracer files')
    chosenFolder = root.directory
    print("chosenFolder:", chosenFolder)
    return chosenFolder


#  Get the contents of a specified directory and build a list of all .utd files
def buildBatchList(chosenFolder):

    listOfTubeDataFilesInDir = []

    for file in os.listdir(chosenFolder):

        if file.endswith(".utd"):
            listOfTubeDataFilesInDir.append(file)

    return listOfTubeDataFilesInDir


# Tube class creates a tube object with all the properly assigned attributes
class Tube:

    def __init__(self, tubeID, xValues, yValues):
        self.tubeID = tubeID
        self.xValues = xValues
        self.yValues = yValues

    def get_tubeID(self):
        return self.tubeID

    def get_xValues(self):
        return self.xValues

    def get_yValues(self):
        return self.yValues


# This function takes a filename argument, looks for that file in the current directory, reads it into a string,
# and edits the string for clarity.  It then creates lists and variables to be used as arguments later when
# the Tube class is instantiated.
def importTubeDataFile(fileToOpen):
    #  File is chosen, now read it into a string and print the string to the screen.
    while True:
        try:

            # Read the contents of the file into a string
            linestring = open(fileToOpen, 'r').read()
            #  Split the string into a list
            tubeDataList = (linestring.split())

            #  Delete the column headers at the front of the text file
            del tubeDataList[0:6]
            del tubeDataList[1]

            # Add "Va" to the 0 position in the list
            tubeDataList.insert(0, "Va")

            anodeVoltage = tubeDataList[1]

            # The rest of the values in the list alternate between voltage and current measurements
            # Therefore, we'll iterate across them in steps of two to separate the voltage from the currents.

            # Create the list of voltages
            xValues = []
            for i in tubeDataList[2::2]:
                xValues.append(i)

            # Create the list of currents
            yValues = []
            for i in tubeDataList[3::2]:
                yValues.append(i)

            # Parse the filename to retrieve the unique ID without the file extension
            tubeID = fileToOpen[:-4]


        #  I left this error handler in from earlier experimentation, but in reality it should never be called
        #  since the read() command looks for files that were just discovered nanoseconds earlier and are most likely
        #  still in the chosenFolder.
        except FileNotFoundError:
            print("The file named ", fileToOpen, " could not be found in the directory.")
            break

        return tubeID, anodeVoltage, xValues, yValues


def main():

    masterTubeDict = {}
    chosenFolder = chooseFolder()  # Prompt the user to choose a folder, then store the path as str(chosenFolder)

    # Change working directory to the chosenFolder
    os.chdir(chosenFolder)

    # Make a batchlist of all the files to be processed
    batchList = buildBatchList(chosenFolder)
    print("The following .utc files were found in the specified directory:")
    print(batchList)
    for tube in batchList:
        print('\n', "Filename", tube, "has been chosen")
        tubeFocus = importTubeDataFile(tube)
        print(tubeFocus)
        tubeID = tubeFocus[0] + '_5749'
        print('The TubeID is', tubeID)
        xValues = tubeFocus[2]
        print("The xValues are", xValues)
        yValues = tubeFocus[3]
        print("The yValues are", yValues)
        tubeObject = Tube(tubeID, xValues, yValues)
        masterTubeDict.update({tubeID: tubeObject})

# Show off the fancy new MasterTubeDict with all the tube objects
    print("\n ...and now to verify that the new tube object is in the MasterTubeDict...")
    keylist = masterTubeDict.keys()
    for key in keylist:
        lookupTube = masterTubeDict[key]
        print("Found tube ", lookupTube.get_tubeID(), "with X values", lookupTube.get_xValues(),
              "and Y values", lookupTube.get_yValues())


    print("\nThe Master Tube Dictionary now contains the following entries:")
    for i in masterTubeDict.keys():
        print(i)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()




