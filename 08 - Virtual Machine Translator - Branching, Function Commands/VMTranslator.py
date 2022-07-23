import sys, os
from VMlib import genOutFileName, genOutFileName_dir, genInFileName_dir
from Parser import parser, CType
from CodeWriter import code_writer, initialize_asm

if len(sys.argv) < 2 :
    print("no file name included")
    exit()

pathName = sys.argv[1]

if pathName[-3] == '.':
    # open file
    fileName = pathName

    fileName_only = os.path.basename(fileName)
    fileName_out = genOutFileName(pathName)

    f_read = open(fileName, 'r')
    f_out = open(fileName_out, 'w')

    # parser
    for line in f_read:
        components = parser(line)
        if not components["type"] == CType.C_WHITESPACE:
            o_line = code_writer(components, fileName_only)
            f_out.write(o_line)


    f_read.close()
    f_out.close()
    print(f"{f_out} is generated")

# if pathName[-1] == '/':
else:
    fileNames = []

    for fileInDir in os.listdir(pathName):
        if fileInDir[-3:] == '.vm':
            fileNames.append(fileInDir)

    fileName_out = genOutFileName_dir(pathName)
    f_out = open(fileName_out, 'w')

    # order
    for i in range(0, len(fileNames)) :
        if fileNames[i] == 'Sys.vm':
            temp = fileNames[i]
            fileNames[i] = fileNames[0]
            fileNames[0] = temp

    # open each file
    for fileName_only in fileNames:
        fileName = genInFileName_dir(pathName, fileName_only)

        f_read = open(fileName, 'r')

        initialize_asm(f_out)

        # parser 
        for line in f_read:
            components = parser(line)
            if not components["type"] == CType.C_WHITESPACE:
                o_line = code_writer(components, fileName_only)
                f_out.write(o_line)

        f_read.close()

    f_out.close()
    print(f"{f_out} is generated")