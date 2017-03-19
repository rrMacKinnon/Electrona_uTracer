

def importTubeData():
    firstTubeFileToOpen = input("Please enter the number of the first tube to plot: ")
    firstTubeFileToOpen = str(firstTubeFileToOpen) + ".utd"
    secondTubeFileToOpen = input("Please enter the number of the second tube to plot: ")
    secondTubeFileToOpen = str(secondTubeFileToOpen) + ".utd"

#  File is chosen, now read it into a string and print the string to the screen.
    while True:
        try:
            firstTube = open(firstTubeFileToOpen, 'r').read()
            print('\n', '\n', "The file ", firstTubeFileToOpen, " contains the following data:")
            print(firstTube)
            secondTube = open(secondTubeFileToOpen, 'r').read()
            print('\n', '\n', "The file ", secondTubeFileToOpen, " contains the following data:")
            print(secondTube)


#  Split the string into a list
            tubeDataList = (linestring.split())

# Add the filename to the list in the 0 position
            tubeDataList.insert(0, fileToOpen)
            print("The file ", fileToOpen, " has the following data points: ", tubeDataList)
            break

        except FileNotFoundError:
            print("Well shit, I couldn't find ", secondTubeFileToOpen, "in the directory.")
        break












def main():
    importTubeData()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
