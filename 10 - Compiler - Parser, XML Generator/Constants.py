from enum import Enum

class TokenType(Enum):
  KEYWORD = 0
  SYMBOL = 1
  IDENTIFIER = 2
  INT_CONST = 3
  STRING_CONST = 4

def typeToStr(typeof):
  if (typeof == TokenType.KEYWORD):
    return "keyword"
  elif (typeof == TokenType.SYMBOL):
    return "symbol"
  elif (typeof == TokenType.IDENTIFIER):
    return "identifier"
  elif (typeof == TokenType.INT_CONST):
    return "integerConstant"
  elif (typeof == TokenType.STRING_CONST):
    return "stringConstant"

KEYWORDS = "class constructor function method field static var int char boolean void true false null this let do if else while return".split(' ')
SYMBOLS = r"{ } ( ) [ ] . , ; + - * / & | < > = ~".split(' ')
COMMENTS = "// /*".split(' ')