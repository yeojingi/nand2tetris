from Parser import CType

g_label = 0
g_var = 0


def initialize_asm(f_out):
    f_out.write(f"// Initialize\n")
    f_out.write(f"@256\nD=A\n@0\nM=D\n")


def code_writer(components, fileName):
    global g_label, g_var
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
    return line

