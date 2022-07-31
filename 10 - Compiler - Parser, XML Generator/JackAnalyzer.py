import sys, os
from lib import getFileNames
from Constants import typeToStr
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

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
    print('25', len(tokenizer.line))
    tokens.append(typeAndToken)
    print('125')

  # show parsing tree
  f_i = open(fileName + ".txt", "w")
  inter = ""
  for ele in tokens:
    inter += typeToStr(ele[0]) + ' ' + ele[1]
    inter += '\n'
  f_i.write(inter)
  f_i.close()
  
  # Generate XML file
  engine = CompilationEngine(tokens)
  xml = engine.CompileClass()

  # print(xml)
  
  f_out.write(xml)

  f_read.close()
  f_out.close()