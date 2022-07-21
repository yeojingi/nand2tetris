import sys, os
from VMlib import genOutFileName
from Parser import parser, CType
from CodeWriter import code_writer, initialize_asm

if len(sys.argv) < 2 :
    print("no file name included")
    exit()

fileName = sys.argv[1]
fileName_only = os.path.basename(fileName)
fileName_out = genOutFileName(fileName)

f_read = open(fileName, 'r')
f_out = open(fileName_out, 'w')

initialize_asm(f_out)

# parser
for line in f_read:
    components = parser(line)
    if not components["type"] == CType.C_WHITESPACE:
        o_line = code_writer(components, fileName_only)
        f_out.write(o_line)


f_read.close()
f_out.close()