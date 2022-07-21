from enum import Enum


class CType(Enum):
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8
    C_WHITESPACE = 9


def parser(line):
    line = line[0:-1]  # new line 제거
    tokens = line.split(' ')

    c_type = get_line_type(tokens)

    if c_type == CType.C_WHITESPACE:
        return {"type": c_type}
    # elif c_type == CType.C_PUSH or c_type == CType.C_POP \
    #         or c_type == CType.C_FUNCTION or c_type == CType.C_CALL:

    arg1 = tokens[0]

    return {"type": c_type, "arg1": arg1, "tokens": tokens}


def get_line_type(tokens):
    token = tokens[0]

    if token == 'push':
        return CType.C_PUSH
    elif token == 'pop':
        return CType.C_POP
    elif token == 'add' or token == 'sub' or token == 'neg' or token == 'eq' or token == 'gt' \
            or token == 'lt' or token == 'and' or token == 'or' or token == 'not':
        return CType.C_ARITHMETIC
    elif token == '//' or token == '':
        return CType.C_WHITESPACE
