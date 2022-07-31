import os

def getFileNames(pathName):
  if pathName[-5] == '.':
    # open file
    fileName = pathName

    fileName_only = os.path.basename(fileName)

    return [fileName[0:-5]]

  else:
    fileNames = []

    if pathName[-1] != '/':
        pathName += '/'

    for fileInDir in os.listdir(pathName):
        if fileInDir[-5:] == '.jack':
            fileNames.append(pathName + fileInDir[0:-5])

    return fileNames