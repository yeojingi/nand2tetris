import os

def genInFileName_dir(pathName, fileName_only):
    if pathName[-1] != '/':
        fileName = pathName+'/'+fileName_only
    else :
        fileName = pathName + fileName_only
    return fileName

def genOutFileName (fileName) :
    return fileName[0:-3] + ".asm"

def genOutFileName_dir (pathName) :
    fileName = os.path.basename(os.path.normpath(pathName))
    fileName += '.asm'
    if pathName[-1] != '/':
        fileName = pathName+'/'+fileName
    else :
        fileName = pathName+fileName
    return fileName