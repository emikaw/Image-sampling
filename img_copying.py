# =========================================== LIBRARIES ===========================================
import os
import shutil
import argparse
from imutils import paths

# =========================================== PARSER ===========================================
# parser = argparse.ArgumentParser()
# parser.add_argument("-l", "--outputDirPath", help="Path to the location where the output folder will be placed")
# parser.add_argument("-p", "--inputPath", help="Path to folder with pictures to be moved")
# parser.add_argument("-n", "--newDirName", help="Name of the new folder with pictures")
# args = vars(parser.parse_args())

# =========================================== FUNCTIONS ===========================================
# Checking if element with name "newDir" exists in targeted folder
def createOutputFolder(newDirName, outputDirPath):
    foldersInNewPath = os.listdir(outputDirPath)
    if newDirName not in foldersInNewPath:
        newDirPath = os.path.join(outputDirPath, newDirName)
        os.mkdir(newDirPath)
        return newDirPath
    else:
        print("Folder already exists")
        question = input("Do you want to set existing folder as a target one? Y/N ")
        if question.capitalize() == "Y":
            newDirPath = os.path.join(outputDirPath, newDirName)
            return newDirPath
        else:
            newDirName = input("Set new name for your directory: ")
            return createOutputFolder(newDirName, outputDirPath)


# Checking if picture with a specific name already exists in output folder
def checkImageExist(newDirPath, pictureName):
    picturesList = os.listdir(newDirPath)
    if pictureName not in picturesList:
        return True
    else:
        print("Image with that name already exists in a target file")
        return False
    
def copyImageToNewLoc(inputPath, pictureName, newDirPath):
    pictureInputPath = os.path.join(inputPath, pictureName) # Path to a picture of interest in input folder
    if checkImageExist(newDirPath, pictureName) == True:
        shutil.copy(pictureInputPath, newDirPath)
        print(f"Image {pictureName} copied successfully")
    else:
        question = input(f"Image {pictureName} already exists in output folder\nDo you want to rename file? Y/N ")
        if question.capitalize() == "Y":   
            imagePrefix, imageSufix = os.path.splitext(pictureName) # We assume that the name of an image look like this: 'nonpc_21_Chr4.ome'
            print(f"Current file name is '{imagePrefix}'")
            newImagePrefix = input(f"\nCurrent file name is '{imagePrefix}\nNew name for your image (try to stick to the convention above): ")
            updatedName = f"{newImagePrefix}{imageSufix}"
            updatedPath = os.path.join(inputPath, updatedName)
            os.rename(pictureInputPath, updatedPath)
            shutil.copy(updatedPath, newDirPath)
            print(f"File {updatedName} copied successfully")
        else:
            print(f"File {pictureName} wasn't copied to the new location")

        

# =========================================== LOOP ===========================================

# if __name__ == "__main__":
#     newDirPath = createOutputFolder(args["newDirName"], args["outputDirPath"])
#     InpDirPicturesList = os.listdir(args["inputPath"])
#     for pictureName in InpDirPicturesList:
#         copyImageToNewLoc(args["inputPath"], pictureName, newDirPath)