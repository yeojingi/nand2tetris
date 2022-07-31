import re
import io
from Constants import TokenType, KEYWORDS, SYMBOLS

class JackTokenizer:
  def __init__(self, file_input):
    line = file_input.read()
    self.line = self.eraseWhiteSpaces(line)
    
  
  def eraseWhiteSpaces(self, line):
    line = re.sub(r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*/', '', line)
    line = re.sub(r'\t', '', line)
    line = re.sub(r'//.*\n', '\n', line)
    return line


  def hasMoreTokens(self):
    # erase space and new-lines
    while len(self.line) > 0:
      print(self.line[0] == '', ord(self.line[0]), self.line[0])
      if self.line[0] == ' ' or self.line[0] == '\n' or self.line[0] == '':
        self.line = self.line[1:]
      else:
        break

    # check if any line is left
    if len(self.line) > 0:
      return True

    return False

  
  def advance(self):
    currentType = self.tokenType()
    
    
    if (currentType == TokenType.KEYWORD):
      element = self.keyword()
    elif (currentType == TokenType.SYMBOL):
      element = self.symbol()
    elif (currentType == TokenType.IDENTIFIER):
      element = self.identifier()
    elif (currentType == TokenType.STRING_CONST):
      element = self.stringVal()
    elif (currentType == TokenType.INT_CONST):
      element = self.intVal()
    else:
      print(currentType)
      exit()

    return [currentType, element]

  
  def tokenType(self):
    # is int const
    if self.line[0].isnumeric():
      return TokenType.INT_CONST

    # is string
    if self.line[0] == '\"':
      return TokenType.STRING_CONST

    # is symbol
    if self.line[0] in SYMBOLS:
      return TokenType.SYMBOL

    i = 0
    while True:
      if not (self.line[i].isalpha() or self.line[i].isnumeric() or self.line[i] == '_'):
        break
      i += 1

    identifier = self.line[0: i]

    # is keyword
    if identifier in KEYWORDS:
      return TokenType.KEYWORD

    # is identifier
    return TokenType.IDENTIFIER
    
  
  def keyword(self):
    i = 0
    while True:
      if not (self.line[i].isalpha() or self.line[i].isnumeric() or self.line[i] == '_'):
        break
      i += 1

    token = self.line[0: i]
    
    # trim self.line
    self.line = self.line[i:]

    return token
  
  def symbol(self):
    token = self.line[0]
    self.line = self.line[1:]
    return token

  def identifier(self):
    i = 0
    while True:
      if not (self.line[i].isalpha() or self.line[i].isnumeric() or self.line[i] == '_'):
        break
      i += 1

    token = self.line[0: i]
    
    # trim self.line
    self.line = self.line[i:]

    return token

  def intVal(self):
    i = 0
    while True:
      if not self.line[i].isnumeric() :
        break
      i += 1

    token = self.line[0: i]
    
    # trim self.line
    self.line = self.line[i:]

    return token

  def stringVal(self):
    i = 1
    while self.line[i] != r'"':
      i += 1

    token = self.line[1: i]
    
    # trim self.line
    self.line = self.line[i+1:]

    return token
