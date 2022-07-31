from Constants import TokenType, typeToStr

class CompilationEngine:
  def __init__(self, tokens):
    self.tokens = tokens
    self.indent = 0

  def hasMoreTokens(self):
    if len(self.tokens) > 0:
      return True
    return False

  def advance(self):
    if self.hasMoreTokens():
      token = self.tokens.pop(0)
      return token
    else:
      exit("없다")

  def printWithIndent(self, str):
    indent = "  "*self.indent
    line = indent + f"{str}"
    return line

  def printTerminal(self, token):
    typestr = typeToStr(token[0])
    terminal = token[1]
    return self.printWithIndent(f"<{typestr}> {terminal} </{typestr}>\n")

  def CompileClass(self):
    typeof = "class"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1
    # keyword - class
    token = self.advance()
    line += self.printTerminal(token)

    # class name
    token = self.advance()
    line += self.printTerminal(token)

    # curly bracket {
    token = self.advance()
    line += self.printTerminal(token)

    # compile Class content
    testToken = self.tokens[0]
    while not (testToken[0] == TokenType.SYMBOL and testToken[1] == '}'):
      if testToken[1] == 'field' or testToken[1] == 'static': 
        line += self.CompileClassVarDec()
      elif testToken[1] == 'constructor' or testToken[1] == 'function' or testToken[1] == 'method': 
        line += self.CompileSubroutine()
      else:
        testToken = self.advance()

      testToken = self.tokens[0]

    
    # curly bracket }
    token = self.advance()
    line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>")
    return line

  def CompileClassVarDec(self):
    typeof = "classVarDec"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # keyword
    token = self.advance()
    line += self.printTerminal(token)

    # variable type
    token = self.advance()
    line += self.printTerminal(token)

    # variable name
    token = self.advance()
    line += self.printTerminal(token)

    # if more vars
    testToken = self.tokens[0]
    print("ClassvarDec , :", testToken)
    while testToken[0] == TokenType.SYMBOL and testToken[1] == ',':
      # ,
      token = self.advance()
      line += self.printTerminal(token)

      # var name
      token = self.advance()
      line += self.printTerminal(token)
      testToken = self.tokens[0]

    # semicolon name
    token = self.advance()
    line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")
    
    return line

  def CompileSubroutine(self):
    typeof = "subroutineDec"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # keyword
    token = self.advance()
    line += self.printTerminal(token)

    # subroutine return type
    token = self.advance()
    line += self.printTerminal(token)

    # subroutine name
    token = self.advance()
    line += self.printTerminal(token)

    # round bracket (
    token = self.advance()
    line += self.printTerminal(token)

    # compile subroutine parameters
    line += self.compileParameterList()

    # round bracket )
    token = self.advance()
    line += self.printTerminal(token)

    # compile subroutine body
    typeof2 = "subroutineBody"

    line += self.printWithIndent(f"<{typeof2}>\n")
    self.indent += 1

    # curly bracket {
    token = self.advance()
    line += self.printTerminal(token)

    # subroutine var dec
    testToken = self.tokens[0]
    while testToken[1] == 'var':
      line += self.compileVarDec()

      testToken = self.tokens[0]

    # subroutine statements
    line += self.compileStatements()

    # curly bracket }
    token = self.advance()
    line += self.printTerminal(token)


    self.indent -= 1
    line += self.printWithIndent(f"</{typeof2}>\n")

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")
    
    return line
  
  def compileParameterList(self):
    typeof = "parameterList"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    testToken = self.tokens[0]
    isFirst = False
    while not (testToken[0] == TokenType.SYMBOL and testToken[1] == ')'):
      if not isFirst:
        # ,
        token = self.advance()
        line += self.printTerminal(token)
      token = self.advance()
      line += self.printTerminal(token)

      testToken = self.tokens[0]
      isFirst = True


    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")
    
    return line

  def compileVarDec(self):
    typeof = "varDec"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # 'var'
    token = self.advance()
    line += self.printTerminal(token)

    # type
    token = self.advance()
    line += self.printTerminal(token)

    # varName
    token = self.advance()
    line += self.printTerminal(token)

    # if more vars
    testToken = self.tokens[0]
    print("varDec , :", testToken)
    while testToken[0] == TokenType.SYMBOL and testToken[1] == ',':
      # ,
      token = self.advance()
      line += self.printTerminal(token)

      # var name
      token = self.advance()
      line += self.printTerminal(token)
      testToken = self.tokens[0]
    
    # ;
    token = self.advance()
    line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileStatements(self):
    typeof = "statements"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    testToken = self.tokens[0]
    isFirst = False
    while not (testToken[0] == TokenType.SYMBOL and testToken[1] == '}'):
      if testToken[1] == 'let':
        line += self.compileLet()
      elif testToken[1] == 'if':
        line += self.compileIf()
      elif testToken[1] == 'while':
        line += self.compileWhile()
      elif testToken[1] == 'do':
        line += self.compileDo()
      elif testToken[1] == 'return':
        line += self.compileReturn()
      else:
        exit(testToken)
      testToken = self.tokens[0]
      

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileDo(self):
    typeof = "doStatement"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # 'do'
    token = self.advance()
    line += self.printTerminal(token)

    # subroutineCall
    line += self.compileSubroutinCall()

    # ;
    token = self.advance()
    line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileLet(self):
    typeof = "letStatement"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # let
    token = self.advance()
    line += self.printTerminal(token)

    # varName
    token = self.advance()
    line += self.printTerminal(token)

    # if '['
    token = self.advance()
    if token[0] == TokenType.SYMBOL and token[1] == '[':
      line += self.printTerminal(token)

      line += self.CompileExpression()
      # print ']'
      token = self.advance()
      line += self.printTerminal(token)

      # '=' to token
      token = self.advance()
    
    # =
    line += self.printTerminal(token)

    line += self.CompileExpression()

    # ;
    token = self.advance()
    line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileWhile(self):
    typeof = "whileStatement"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # 'while'
    token = self.advance()
    line += self.printTerminal(token)

    # (
    token = self.advance()
    line += self.printTerminal(token)

    line += self.CompileExpression()

    # )
    token = self.advance()
    line += self.printTerminal(token)
    print(line)
    # {
    token = self.advance()
    line += self.printTerminal(token)

    line += self.compileStatements()

    # }
    token = self.advance()
    line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileReturn(self):
    typeof = "returnStatement"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # 'return'
    token = self.advance()
    line += self.printTerminal(token)


    testToken = self.tokens[0]
    if testToken[1] != ';':
      line += self.CompileExpression()

    # ;
    token = self.advance()
    line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")


    return line

  def compileIf(self):
    typeof = "ifStatement"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # 'if'
    token = self.advance()
    line += self.printTerminal(token)

    # (
    token = self.advance()
    line += self.printTerminal(token)

    line += self.CompileExpression()

    # )
    token = self.advance()
    line += self.printTerminal(token)

    # {
    token = self.advance()
    line += self.printTerminal(token)

    line += self.compileStatements()

    # }
    token = self.advance()
    line += self.printTerminal(token)

    testToken = self.tokens[0]
    if testToken[1] == 'else':
      # 'else'
      token = self.advance()
      line += self.printTerminal(token)

      # {
      token = self.advance()
      line += self.printTerminal(token)

      line += self.compileStatements()

      # }
      token = self.advance()
      line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def CompileExpression(self):
    typeof = "expression"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # TODO: complete this function
    # token = self.advance()
    # line += self.printTerminal(token)

    line += self.CompileTerm()

    testToken = self.tokens[0]
    if testToken[1] in '+ - * / & | < > ='.split(' '):
      token = self.advance()
      if token[1] == '<':
        token[1] = '&lt;'
      elif token[1] == '>':
        token[1] = '&gt;'
      elif token[1] == r'"':
        token[1] = '&quot;'
      elif token[1] == '&':
        token[1] = '&amp;'
      line += self.printTerminal(token)
      line += self.CompileTerm()

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def CompileTerm(self):
    typeof = "term"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    testToken = self.tokens[0]
    if testToken[0] == TokenType.INT_CONST:
      token = self.advance()
      line += self.printTerminal(token)
    elif testToken[0] == TokenType.STRING_CONST:
      token = self.advance()
      line += self.printTerminal(token)
    elif testToken[0] == TokenType.KEYWORD:
      # true, false, null, this
      token = self.advance()
      line += self.printTerminal(token)
    elif testToken[0] == TokenType.SYMBOL:
      if testToken[1] == '(':
        # (
        token = self.advance()
        line += self.printTerminal(token)

        line += self.CompileExpression()

        # )
        token = self.advance()
        line += self.printTerminal(token)
      # - ~
      elif testToken[1] == '-' or testToken[1] == '~':
        token = self.advance()
        line += self.printTerminal(token)
        line += self.CompileTerm()
    elif testToken[0] == TokenType.IDENTIFIER:
      llToken = self.tokens[1]
      # subroutine call
      if llToken[1] == '(' or llToken[1] == '.':
        line += self.compileSubroutinCall()

      # array call
      elif llToken[1] == '[':
        # var name
        token = self.advance()
        line += self.printTerminal(token)

        # [
        token = self.advance()
        line += self.printTerminal(token)

        line += self.CompileExpression()

        # ]
        token = self.advance()
        line += self.printTerminal(token)

      else:
        # var name
        token = self.advance()
        line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def CompileExpressionList(self):
    typeof = "expressionList"
    # print(typeof)

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    testToken = self.tokens[0]
    if testToken[1] != ')':
      line += self.CompileExpression()
      testToken = self.tokens[0]
      while testToken[1] == ',':
        # ,
        token = self.advance()
        line += self.printTerminal(token)

        line += self.CompileExpression()
        testToken = self.tokens[0]

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileSubroutinCall(self):
    # print("compile subroutine call")
    llToken = self.tokens[1]
    line = ""
      
    if llToken[1] == '.':
      # var or class name
      token = self.advance()
      line += self.printTerminal(token)

      # .
      token = self.advance()
      line += self.printTerminal(token)

    # subroutine name
    token = self.advance()
    line += self.printTerminal(token)

    # (
    token = self.advance()
    line += self.printTerminal(token)

    line += self.CompileExpressionList()

    # )
    token = self.advance()
    line += self.printTerminal(token)
    return line