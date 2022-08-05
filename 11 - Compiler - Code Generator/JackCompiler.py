import sys, os
from lib import getFileNames
from Constants import typeToStr
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from VMWriter import VMWriter

if len(sys.argv) < 2 :
    print("no file name included")
    exit()

pathName = sys.argv[1]
fileNames = getFileNames(pathName)
for fileName in fileNames:
  f_read = open(fileName + ".jack", 'r')
  f_out = open(fileName + ".xml", 'w')
  tokens = []

  # Analyze Jack
  tokenizer = JackTokenizer(f_read)
  while tokenizer.hasMoreTokens():
    typeAndToken = tokenizer.advance()
    tokens.append(typeAndToken)

  # Generate XML file
  vmWriter = VMWriter(fileName)
  engine = CompilationEngine(tokens, vmWriter)
  xml = engine.CompileClass()

  # print(xml)
  
  f_out.write(xml)

  f_read.close()
  f_out.close()