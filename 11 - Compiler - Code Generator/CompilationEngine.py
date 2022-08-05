from Constants import TokenType, typeToStr, KEYWORDS
from SymbolTable import SymbolTable

class CompilationEngine:
  def __init__(self, tokens, vmWriter):
    self.tokens = tokens
    self.indent = 0
    self.symbolTable = SymbolTable()
    self.className = ''
    self.vmWriter = vmWriter
    self.n = 0
    self.labelNum = 0

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

  def getLabel(self):
    label = self.className + "$"
    label += str(self.labelNum)
    self.labelNum += 1
    return label

  def printIndent(self):
    indent = "  "*self.indent
    return line

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

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1
    # keyword - class
    token = self.advance()
    line += self.printTerminal(token)

    # class name
    token = self.advance()
    line += self.printTerminal(token)
    self.className = token[1]

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

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile

    # variable declaration
    # get keyword
    token = self.advance()
    varKind = token[1]

    # get type
    token = self.advance()
    varType = token[1]

    # type은 출력해야 돼
    line += self.printTerminal(token)

    # get name
    token = self.advance()
    varName = token[1]

    # new declaration
    varDec = 'declare ' + varKind + ' ' + varName

    newToken = [TokenType.IDENTIFIER, varDec]
    line += self.printTerminal(newToken)

    # add to symbol table
    self.symbolTable.define(varName, varType, varKind)

    # if more vars
    testToken = self.tokens[0]
    while testToken[0] == TokenType.SYMBOL and testToken[1] == ',':
      # ,
      token = self.advance()
      line += self.printTerminal(token)

      # var name
      token = self.advance()
      
      varName = token[1]
      varDec = 'declare ' + varKind + ' ' + varName
      newToken = [TokenType.IDENTIFIER, varDec]
      line += self.printTerminal(newToken)
      
      self.symbolTable.define(varName, varType, varKind)

      testToken = self.tokens[0]

    # semicolon name
    token = self.advance()
    line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")
    
    return line

  def CompileSubroutine(self):
    typeof = "subroutineDec"
    self.symbolTable.startSubroutine()

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # keyword
    token = self.advance()
    line += self.printTerminal(token)
    keyword = token[1]
    if keyword == 'method':
      self.symbolTable.define("this", self.className, "argument")

    # subroutine return type
    token = self.advance()
    line += self.printTerminal(token)

    # subroutine name
    token = self.advance()
    line += self.printTerminal(token)
    subroutineName = token[1]

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
    self.n = 0
    testToken = self.tokens[0]
    while testToken[1] == 'var':
      line += self.compileVarDec()

      testToken = self.tokens[0]

    # vm writer
    self.vmWriter.writeFunction(self.className + "." + subroutineName, self.n)

    # if constructor
    if keyword == 'constructor':
      numAlloc = self.symbolTable.varCount('field') + self.symbolTable.varCount('static')
      for i in range(0, numAlloc):
        self.vmWriter.writePush("constant", 0)
      self.vmWriter.writePush("constant", numAlloc)
      self.vmWriter.writeCall("Memory.alloc", 1)
      self.vmWriter.writePop("pointer", 0)
    elif keyword == 'method':
      self.vmWriter.writePush("argument", 0)
      self.vmWriter.writePop("pointer", 0)

    # /vm writer

    # subroutine statements
    line += self.compileStatements()

    # curly bracket }
    token = self.advance()
    line += self.printTerminal(token)


    self.indent -= 1
    line += self.printWithIndent(f"</{typeof2}>\n")

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")
    
    print(f"{self.className}.{subroutineName}'s symbol table")
    self.symbolTable.showTables()
    return line
  
  def compileParameterList(self):
    typeof = "parameterList"

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    testToken = self.tokens[0]
    isFirst = True
    while not (testToken[0] == TokenType.SYMBOL and testToken[1] == ')'):
      if not isFirst:
        # ,
        token = self.advance()
        line += self.printTerminal(token)

      # type
      token = self.advance()
      line += self.printTerminal(token)
      varType = token[1]

      # var Name
      token = self.advance()
      line += self.printTerminal(token)
      varName = token[1]
      # print(varType)

      # token = self.advance()
      # line += self.printTerminal(token)
      # print("n", varName)

      self.n += 1
      self.symbolTable.define(varName, varType, "argument")

      testToken = self.tokens[0]
      isFirst = False


    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")
    
    return line

  def compileVarDec(self):
    typeof = "varDec"
    
    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # variable declaration
    # get keyword
    token = self.advance()
    varKind = token[1]

    # get type
    token = self.advance()
    varType = token[1]

    # type은 출력해야 돼
    line += self.printTerminal(token)

    # get name
    token = self.advance()
    varName = token[1]

    # new declaration
    varDec = 'declare ' + varKind + ' ' + varName

    newToken = [TokenType.IDENTIFIER, varDec]
    line += self.printTerminal(newToken)

    # add to symbol table
    self.symbolTable.define(varName, varType, varKind)
    self.n += 1

    # if more vars
    testToken = self.tokens[0]
    while testToken[0] == TokenType.SYMBOL and testToken[1] == ',':
      # ,
      token = self.advance()
      line += self.printTerminal(token)

      # var name
      token = self.advance()

      varName = token[1]
      varDec = 'declare ' + varKind + ' ' + varName
      newToken = [TokenType.IDENTIFIER, varDec]
      line += self.printTerminal(newToken)
      self.symbolTable.define(varName, varType, varKind)
      self.n += 1

      testToken = self.tokens[0]
    
    # ;
    token = self.advance()
    line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileStatements(self):
    typeof = "statements"
    
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
        print("CompilationEngine.py Error compileStatements: ", end="")
        exit(testToken)
      testToken = self.tokens[0]
      

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileDo(self):
    typeof = "doStatement"    

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # 'do'
    token = self.advance()
    line += self.printTerminal(token)

    # subroutineCall
    line += self.compileSubroutineCall()

    # ;
    token = self.advance()
    line += self.printTerminal(token)

    self.vmWriter.writePop("temp", "0")

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileLet(self):
    typeof = "letStatement"
    isArray = False
    
    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # let
    token = self.advance()
    line += self.printTerminal(token)

    # varName
    token = self.advance()
    varName = token[1]
    varKind = self.symbolTable.kindOf(varName)
    index = self.symbolTable.indexOf(varName)
    newTerminal = "use " + varKind + " " + varName
    newToken = [TokenType.IDENTIFIER, newTerminal]
    line += self.printTerminal(newToken)

    # if '['
    token = self.advance()
    if token[0] == TokenType.SYMBOL and token[1] == '[':
      if varKind == 'var':
        self.vmWriter.writePush("local", index)
      elif varKind == 'argument':
        self.vmWriter.writePush("argument", index) 
      elif varKind == 'static':
        self.vmWriter.writePush("static", index)
      elif varKind == 'field':
        self.vmWriter.writePush("this", index)

      isArray = True
      line += self.printTerminal(token)

      line += self.CompileExpression()
      # print ']'
      token = self.advance()
      line += self.printTerminal(token)

      self.vmWriter.writeArithmetic("add")

      # '=' to token
      token = self.advance()

    # =
    line += self.printTerminal(token)

    line += self.CompileExpression()


    # vm writer
    if isArray:
      self.vmWriter.writePop("temp", 0)
      self.vmWriter.writePop("pointer", 1)
      self.vmWriter.writePush("temp", 0)
      self.vmWriter.writePop("that", 0)
    elif varKind == 'var':
      self.vmWriter.writePop("local", index)
    elif varKind == 'argument':
      self.vmWriter.writePop("argument", index) 
    elif varKind == 'static':
      self.vmWriter.writePop("static", index)
    elif varKind == 'field':
      self.vmWriter.writePop("this", index)
    # /vm writer

    # ;
    token = self.advance()
    line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileWhile(self):
    typeof = "whileStatement"

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    label1 = self.getLabel()
    label2 = self.getLabel()

    self.vmWriter.writeLabel(label1)

    # compile
    # 'while'
    token = self.advance()
    line += self.printTerminal(token)

    # (
    token = self.advance()
    line += self.printTerminal(token)

    line += self.CompileExpression()

    self.vmWriter.writeArithmetic("not")
    self.vmWriter.writeIf(label2)

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

    self.vmWriter.writeGoto(label1)
    self.vmWriter.writeLabel(label2)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileReturn(self):
    typeof = "returnStatement"

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    # 'return'
    token = self.advance()
    line += self.printTerminal(token)

    # TODO: Expression push

    testToken = self.tokens[0]
    if testToken[1] != ';':
      line += self.CompileExpression()
    else:
      self.vmWriter.writePush("constant", 0)

    # vm writer
    self.vmWriter.writeReturn()
    # /vm writer

    # ;
    token = self.advance()
    line += self.printTerminal(token)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")


    return line

  def compileIf(self):
    typeof = "ifStatement"

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    label1 = self.getLabel()
    label2 = self.getLabel()


    # compile
    # 'if'
    token = self.advance()
    line += self.printTerminal(token)

    # (
    token = self.advance()
    line += self.printTerminal(token)

    line += self.CompileExpression()

    self.vmWriter.writeArithmetic('not')
    self.vmWriter.writeIf(label1)

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

    self.vmWriter.writeGoto(label2)

    self.vmWriter.writeLabel(label1)

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

    self.vmWriter.writeLabel(label2)

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def CompileExpression(self):
    typeof = "expression"
    op = 0

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    line += self.CompileTerm()

    testToken = self.tokens[0]
    if testToken[1] in '+ - * / & | < > ='.split(' '):
      token = self.advance()
      op = token[1]
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

      # vm writer
      if op == '+':
        self.vmWriter.writeArithmetic("add")
      elif op == '-':
        self.vmWriter.writeArithmetic("sub")
      elif op == '=':
        self.vmWriter.writeArithmetic("eq")
      elif op == '>':
        self.vmWriter.writeArithmetic("gt")
      elif op == '<':
        self.vmWriter.writeArithmetic("lt")
      elif op == '&':
        self.vmWriter.writeArithmetic("and")
      elif op == '|':
        self.vmWriter.writeArithmetic("or")
      elif op == '*':
        self.vmWriter.writeCall("Math.multiply", "2")
      elif op == '/':
        self.vmWriter.writeCall("Math.divide", "2")
      # /vm writer

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def CompileTerm(self):
    typeof = "term"

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    testToken = self.tokens[0]
    if testToken[0] == TokenType.INT_CONST:
      token = self.advance()
      line += self.printTerminal(token)

      self.vmWriter.writePush("constant", token[1])
    elif testToken[0] == TokenType.STRING_CONST:
      token = self.advance()
      line += self.printTerminal(token)

      string = token[1]
      length = len(string)

      self.vmWriter.writePush("constant", length)
      self.vmWriter.writeCall("String.new", 1)
      for i in range(0, length):
        self.vmWriter.writePush("constant", ord(string[i]))
        self.vmWriter.writeCall("String.appendChar", 2)
    elif testToken[0] == TokenType.KEYWORD:
      # true, false, null, this
      token = self.advance()
      line += self.printTerminal(token)
      
      keyword = token[1]
      if keyword == 'true':
        self.vmWriter.writePush("constant", "1")
        self.vmWriter.writeArithmetic('neg')
      elif keyword == 'false':
        self.vmWriter.writePush("constant", "0")
      elif keyword == 'null':
        self.vmWriter.writePush("constant", "0")
      elif keyword == 'this':
        self.vmWriter.writePush("pointer", "0")

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

        ## vm writer
        if testToken[1] == '-':
          self.vmWriter.writeArithmetic("neg")
        elif testToken[1] == '~':
          self.vmWriter.writeArithmetic("not")
        ## /vm writer
    elif testToken[0] == TokenType.IDENTIFIER:
      llToken = self.tokens[1]
      # subroutine call
      if llToken[1] == '(' or llToken[1] == '.':
        line += self.compileSubroutineCall()

      # array call
      elif llToken[1] == '[':
        # var name
        token = self.advance()
        varName = token[1]
        varKind = self.symbolTable.kindOf(varName)
        newTerminal = "use " + varKind + " " + varName
        newToken = [TokenType.IDENTIFIER, newTerminal]
        line += self.printTerminal(newToken)

        index = self.symbolTable.indexOf(varName)
        if varKind == 'var':
          self.vmWriter.writePush("local", index)
        elif varKind == 'argument':
          self.vmWriter.writePush("argument", index) 
        elif varKind == 'static':
          self.vmWriter.writePush("static", index) 
        elif varKind == 'field':
          self.vmWriter.writePush("this", index) 

        # [
        token = self.advance()
        line += self.printTerminal(token)

        line += self.CompileExpression()
        self.vmWriter.writeArithmetic("add")
        self.vmWriter.writePop("pointer", 1)
        self.vmWriter.writePush("that", 0)

        # ]
        token = self.advance()
        line += self.printTerminal(token)

      else:
        # var name
        token = self.advance()
        varName = token[1]
        varKind = self.symbolTable.kindOf(varName)
        newTerminal = "use " + varKind + " " + varName
        newToken = [TokenType.IDENTIFIER, newTerminal]
        line += self.printTerminal(newToken)

        index = self.symbolTable.indexOf(varName)
        if varKind == 'var':
          self.vmWriter.writePush("local", index)
        elif varKind == 'argument':
          self.vmWriter.writePush("argument", index) 
        elif varKind == 'static':
          self.vmWriter.writePush("static", index) 
        elif varKind == 'field':
          self.vmWriter.writePush("this", index) 

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def CompileExpressionList(self):
    typeof = "expressionList"
    self.n = 0

    line = self.printWithIndent(f"<{typeof}>\n")
    self.indent += 1

    # compile
    testToken = self.tokens[0]
    if testToken[1] != ')':
      line += self.CompileExpression()
      testToken = self.tokens[0]

      self.n += 1
      while testToken[1] == ',':
        # ,
        token = self.advance()
        line += self.printTerminal(token)

        line += self.CompileExpression()
        testToken = self.tokens[0]
        self.n += 1

    self.indent -= 1
    line += self.printWithIndent(f"</{typeof}>\n")

    return line

  def compileSubroutineCall(self):
    llToken = self.tokens[1]
    line = ""
    calleeName = ""
    addThisArg = 0
      
    if llToken[1] == '.':
      # var or class name
      token = self.advance()
      newTerminal = "use "

      # class
      if self.symbolTable.kindOf(token[1]) == 'none':
        newTerminal += "class " + token[1]
        calleeName = token[1] + "."
      # var
      else:
        newTerminal += "var " + token[1]
        
        # this 추가
        varName = token[1]
        varType = self.symbolTable.typeOf(varName)
        varKind = self.symbolTable.kindOf(varName)

        # TODO: field에서 에러날 듯..?
        if varKind == 'var':
          varKind = 'local'
        elif varKind == 'field':
          varKind = 'this'
        varIndex = self.symbolTable.indexOf(varName)
        self.vmWriter.writePush(varKind, varIndex)

        calleeName = varType + "."
        addThisArg = 1

      newToken = [TokenType.IDENTIFIER, newTerminal]
      line += self.printTerminal(newToken)

      # .
      token = self.advance()
      line += self.printTerminal(token)

      # subroutine name
      token = self.advance()
      newTerminal = "use subroutine " + token[1]
      newToken = [TokenType.IDENTIFIER, newTerminal]
      line += self.printTerminal(newToken)

      calleeName += token[1]
    
    # if no class name nor var name -> method call
    else:
      # subroutine name
      token = self.advance()
      newTerminal = "use subroutine " + token[1]
      newToken = [TokenType.IDENTIFIER, newTerminal]
      line += self.printTerminal(newToken)
      calleeName += self.className + "."

      calleeName += token[1]

      self.vmWriter.writePush('pointer', 0)
      addThisArg = 1

    # (
    token = self.advance()
    line += self.printTerminal(token)

    line += self.CompileExpressionList()

    # )

    # vm writer
    self.vmWriter.writeCall(calleeName, self.n + addThisArg)

    # /vm writer
    token = self.advance()
    line += self.printTerminal(token)
    return line