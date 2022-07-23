from Parser import CType

g_label = 0
g_var = 0
g_function_name = ""
g_ret = 0

def initialize_asm(f_out):
    f_out.write(f"@256 // Initialize\n")
    f_out.write(f"D=A\n@0\nM=D\n")
    f_out.write(code_writer({"type": CType.C_CALL, "tokens":['call', 'Sys.init', '0']}, ''))


def code_writer(components, fileName):
    global g_label, g_var, g_function_name, g_ret
    fileName = fileName[0:-3]
    c_type = components["type"]
    registers = {'local': 1, 'argument': 2, 'this': 3, 'that': 4}

    if c_type == CType.C_PUSH:
        arg = int(components["tokens"][2])
        push_type = components["tokens"][1]
        if push_type == 'constant':
            line = f"@{arg} // PUSH CONSTANT {arg}\n"
            line += f'D=A\n'
            line += f'@0\nA=M\nM=D\n'
            line += f"@0\nM=M+1\n"
        elif push_type in registers.keys():
            reg_address = registers[push_type]
            line = f"@{reg_address} // PUSH {push_type} {arg}\n"
            # save @1
            line += f'D=M\n'
            line += f'@{arg}\nA=D+A\nD=M\n'
            line += f'@0\nA=M\nM=D\n'
            line += f"@0\nM=M+1\n"
        elif push_type == 'temp':
            arg += 5
            line = f"@{arg} // PUSH TEMP {arg}\n"
            line += f'D=M\n'
            line += f'@0\nA=M\nM=D\n'
            line += f"@0\nM=M+1\n"
        elif push_type == 'pointer':
            arg += 3
            line = f"@{arg} // PUSH POINTER {arg-3}\n"
            line += f'D=M\n'
            line += f'@0\nA=M\nM=D\n'
            line += f"@0\nM=M+1\n"
        elif push_type == 'static':
            static_var = fileName + '.' + str(arg)
            line = f"@{static_var} // PUSH STATIC {arg}\n"
            line += f'D=M\n'
            line += f'@0\nA=M\nM=D\n'
            line += f"@0\nM=M+1\n"
        else:
            pass
    elif c_type == CType.C_POP:
        arg = int(components["tokens"][2])
        pop_type = components["tokens"][1]
        if pop_type == 'constant':
            line = f"@0 // POP\n"
            line += f"M=M-1\n"
            line += f"A=M\nD=M\n"
            line += f"@{arg}\nM=D\n"
        elif pop_type in registers.keys():
            reg_address = registers[pop_type]
            line = f"@{reg_address} // POP {pop_type} {arg}\n"
            line += f"A=M\nD=A\n"
            line += f"@{arg}\nA=D+A\nD=A\n@P{g_var}\nM=D\n"
            line += f"@0\nM=M-1\nA=M\nD=M\n"
            line += f"@P{g_var}\nA=M\nM=D\n"

            g_var += 1
        elif pop_type == 'temp':
            arg += 5
            line = f"@0 // POP TEMP {arg-5}\n"
            line += f"M=M-1\nA=M\nD=M\n"
            line += f"@{arg}\nM=D\n"
        elif pop_type == 'pointer':
            arg += 3
            line = f"@0 // POP POINTER {arg-3}\n"
            line += f"M=M-1\nA=M\nD=M\n"
            line += f"@{arg}\nM=D\n"
        elif pop_type == 'static':
            static_var = fileName + '.' + str(arg)
            line = f"@0 // POP STATIC {arg}\n"
            line += f"M=M-1\nA=M\nD=M\n"
            line += f"@{static_var}\nM=D\n"
    elif c_type == CType.C_ARITHMETIC:
        arg = components["arg1"]
        line = f"@0// @{arg}\n"
        if arg == 'add':
            line += f"M=M-1\nA=M\nD=M\n"
            line += f"@0\nM=M-1\nA=M\nM=M+D\n@0\nM=M+1\n"
        if arg == 'sub':
            line += f"M=M-1\nA=M\nD=M\n"
            line += f"@0\nM=M-1\nA=M\nM=M-D\n@0\nM=M+1\n"
        if arg == 'neg':
            line += f"M=M-1\nA=M\nM=-M\n"
            line += f"@0\nM=M+1\n"
        if arg == 'eq':
            line += f"M=M-1\nA=M\nD=M\n"
            line += f"@0\nM=M-1\nA=M\nM=M-D\nD=M\nM=-1\n@E{g_label}\nD;JEQ\n"
            line += f"@0\nA=M\nM=0\n(E{g_label})\n@0\nM=M+1\n"
            g_label += 1
        if arg == 'lt':
            line += f"M=M-1\nA=M\nD=M\n"
            line += f"@0\nM=M-1\nA=M\nM=M-D\nD=M\nM=-1\n@E{g_label}\nD;JLT\n"
            line += f"@0\nA=M\nM=0\n(E{g_label})\n@0\nM=M+1\n"
            g_label += 1
        if arg == 'gt':
            line += f"M=M-1\nA=M\nD=M\n"
            line += f"@0\nM=M-1\nA=M\nM=M-D\nD=M\nM=-1\n@E{g_label}\nD;JGT\n"
            line += f"@0\nA=M\nM=0\n(E{g_label})\n@0\nM=M+1\n"
            g_label += 1
        if arg == 'and':
            line += f"M=M-1\nA=M\nD=M\n"
            line += f"@0\nM=M-1\nA=M\nM=M&D\n@0\nM=M+1\n"
        if arg == 'or':
            line += f"M=M-1\nA=M\nD=M\n"
            line += f"@0\nM=M-1\nA=M\nM=M|D\n@0\nM=M+1\n"
        if arg == 'not':
            line += f"M=M-1\nA=M\nM=!M\n"
            line += f"@0\nM=M+1\n"
    elif c_type == CType.C_LABEL:
        label = components["tokens"][1]
        if g_function_name != "":
            label = g_function_name + '$' + label
        line = f"({label}) // label {label}\n"
    elif c_type == CType.C_GOTO:
        label = components["tokens"][1]
        if g_function_name != "":
            label = g_function_name + '$' + label
        line = f"@{label}\n0;JMP // goto {label}\n"
    elif c_type == CType.C_IF:
        label = components["tokens"][1]
        if g_function_name != "":
            label = g_function_name + '$' + label
        line = f"@0 // if-goto {label}\n"
        line += f"M=M-1\nA=M\nD=M\n@{label}\nD;JNE\n"
    elif c_type == CType.C_FUNCTION:
        fName = components["tokens"][1]
        nArgs = components["tokens"][2]
        g_function_name = fName
        line = f"({fName}) // function {fName} declaration\n"
        for i in range(0, int(nArgs)) :
            line += f"@SP // initialize local var {i} time(s)\nA=M\nM=0\n@SP\nM=M+1\n"
    elif c_type == CType.C_RETURN:
        line = f"@LCL // return | FRAME = LCL\n"
        line += f"D=M\n"
        line += f"@FRAME\n"
        line += f"M=D\n"
        line += f"@5 // RET = *(FRAME-5)\n"
        line += f"A=D-A\nD=M\n"
        line += f"@RET\n"
        line += f"M=D\n"
        line += f"@SP // *ARG = pop()\n"
        line += f"M=M-1\nA=M\nD=M\n"
        line += f"@ARG\nA=M\nM=D\n"
        line += f"@ARG// SP = ARG+1\n"
        line += f"D=M\nD=D+1\n@SP\nM=D\n"
        line += f"@FRAME // THAT = *(FRAME-1)\n"
        line += f"D=M\nD=D-1\nA=D\nD=M\n@THAT\nM=D\n"
        line += f"@FRAME // THIS = *(FRAME-2)\n"
        line += f"D=M\nD=D-1\nD=D-1\nA=D\nD=M\n@THIS\nM=D\n"
        line += f"@FRAME // ARG = *(FRAME-3)\n"
        line += f"D=M\nD=D-1\nD=D-1\nD=D-1\nA=D\nD=M\n@ARG\nM=D\n"
        line += f"@FRAME // LCL = *(FRAME-4)\n"
        line += f"D=M\nD=D-1\nD=D-1\nD=D-1\nD=D-1\nA=D\nD=M\n@LCL\nM=D\n"
        line += f"@RET // goto RET\n"
        line += f"A=M\n0;JMP\n"
    elif c_type == CType.C_CALL:
        fName = components["tokens"][1]
        nArgs = components["tokens"][2]
        ret = fName + '$ret.' + str(g_ret) 
        line = f"@{ret} // call {fName} {nArgs} | push return-address\n"
        line += f"D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        line += f"@LCL // push LCL\n"
        line += f"D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        line += f"@ARG // push ARG\n"
        line += f"D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        line += f"@THIS // push THIS\n"
        line += f"D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        line += f"@THAT // push THAT\n"
        line += f"D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        line += f"@SP// ARG = SP-n-5\n"
        line += f"D=M\nD=D-1\nD=D-1\nD=D-1\nD=D-1\nD=D-1\n"
        for i in range(0, int(nArgs)) :
            line += f"D=D-1 // subtract {i} times\n"
        line += f"@ARG\nM=D\n"
        line += f"@SP // LCL = SP\n"
        line += f"D=M\n@LCL\nM=D\n"
        line += f"@{fName} // goto f\n"
        line += f"0;JMP\n"
        line += f"({ret})\n"
        g_ret += 1
    else:
        print(f"CodeWriter.py has an error with {fileName}.vm: Found undefined command")
        print(components)
        exit(1)
    return line

