class VMWriter:
  def __init__(self, fileName):
    self.f_out = open(fileName + ".vm", 'w')

  def writeComment(self, comment):
    self.f_out.write(f"// {comment}\n")

  def writePush(self, segment, index):
    self.f_out.write(f"push {segment} {index}\n")

  def writePop(self, segment, index):
    self.f_out.write(f"pop {segment} {index}\n")
  
  def writeArithmetic(self, command):
    self.f_out.write(f"{command}\n")

  def writeLabel(self, label):
    self.f_out.write(f"label {label}\n")

  def writeGoto(self, label):
    self.f_out.write(f"goto {label}\n")

  def writeIf(self, label):
    self.f_out.write(f"if-goto {label}\n")

  def writeCall(self, name, nArgs):
    self.f_out.write(f"call {name} {nArgs}\n")

  def writeFunction(self, name, nLocals):
    self.f_out.write(f"function {name} {nLocals}\n")

  def writeReturn(self):
    self.f_out.write(f"return\n")

  def close(self):
    self.f_out.close()