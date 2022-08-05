TYPE = 0
KIND = 1
INDEX = 2

class SymbolTable:
  def __init__(self):
    self.classTable = {}
    self.subroutineTable = {}

    self.indices = {
      "static": 0,
      "field": 0,
      "var": 0,
      "argument": 0,
    }

  def showTables(self):
    print("=== class table ===")
    for key, val in self.classTable.items():
      print(key, val)
    print("=== subroutine table ===")
    for key, val in self.subroutineTable.items():
      print(key, val)
    print("======================\n")

  def startSubroutine(self):
    self.subroutineTable = {}
    self.indices["var"] = 0
    self.indices["argument"] = 0

  def define(self, name, typeName, kind):
    index = self.varCount(kind)
    var = []
    var.append(typeName)


    if kind == "static" or kind == "field":
      self.classTable[name] = [typeName, kind, index]
    elif kind == "argument" or kind == "var":
      self.subroutineTable[name] = [typeName, kind, index]

  def varCount(self, kind):
    index = self.indices[kind]
    self.indices[kind] += 1
    return index

  def kindOf(self, name):
    for key, val in self.subroutineTable.items():
      if key == name:
        return val[KIND]
    for key, val in self.classTable.items():
      if key == name:
        return val[KIND]
    return "none"

  def typeOf(self, name):
    for key, val in self.subroutineTable.items():
      if key == name:
        return val[TYPE]
    for key, val in self.classTable.items():
      if key == name:
        return val[TYPE]

  def indexOf(self, name):
    for key, val in self.subroutineTable.items():
      if key == name:
        return val[INDEX]
    for key, val in self.classTable.items():
      if key == name:
        return val[INDEX]
        