# =========================================== LIBRARIES ===========================================
import argparse
import os
import random
import shutil
from img_copying import createOutputFolder, checkImageExist, copyImageToNewLoc

# =========================================== PARSER ===========================================
parser = argparse.ArgumentParser()
parser.add_argument("-pf", "--pathDir1", help="Path to the location of first folder with data")
parser.add_argument("-ps", "--pathDir2", help="Path to the location of second folder with data")
parser.add_argument("-n", "--newDirName", help="Name of the new folder with pictures")
parser.add_argument("-l", "--outputDirPath", help="Path to the location where the output folder will be placed")
args = vars(parser.parse_args())

# =========================================== FUNCTIONS ===========================================

imagesList1 = os.listdir(args["pathDir1"])
imagesCount1 = len(imagesList1)

imagesList2 = os.listdir(args["pathDir2"])
imagesCount2 = len(imagesList2)

newDirectoryPath = createOutputFolder(args["newDirName"], args["outputDirPath"])
newDirectoryList = os.listdir(newDirectoryPath)
newDirectoryCount = len(newDirectoryList)

repeats = min(imagesCount1, imagesCount2)

if imagesCount1 > imagesCount2 and newDirectoryCount < imagesCount2:
     randomImageList = []
     for i in range(repeats+1):
         randomImageName = random.choice(imagesList1)
         if randomImageName not in randomImageList:
            copyImageToNewLoc(args["pathDir1"], randomImageName, newDirectoryPath)
            newDirectoryCount += 1
            randomImageList.append(randomImageName)
         else:
            repeats += 1
            pass

elif imagesCount2 > imagesCount1 and newDirectoryCount < imagesCount1:
    randomImageList = []
    repeats = min(imagesCount1, imagesCount2)
    print(repeats)
    for i in range(repeats+1):
        randomImageName = random.choice(imagesList2)
        if randomImageName not in randomImageList:
            copyImageToNewLoc(args["pathDir2"], randomImageName, newDirectoryPath)
            newDirectoryCount += 1
            randomImageList.append(randomImageName)
        else:
            repeats += 1
            pass

else:
    pass

            

