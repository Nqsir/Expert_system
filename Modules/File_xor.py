from Header.Header import *

from Modules.File_useful_function import search_regex, get_param


# ------------------------------------------------------------------------------------------------------------------
#   XOR handling function
# ------------------------------------------------------------------------------------------------------------------
def operation_xor(line, group):
    # XOR occurrences checking loop
    flag_regex_pair_xor = 1
    while flag_regex_pair_xor == 1:
        # Rule copy
        tmp_xor_copy = line
        tuple_regex_pair_xor = search_regex(group, CONST_REGEX_PAIR_XOR)
        for n, pair_xor in enumerate(tuple_regex_pair_xor):
            param = get_param(pair_xor)
            rep = calc_xor(param[0], param[1])
            line = line.replace(tuple_regex_pair_xor[n], rep)
        if tmp_xor_copy == line:
            flag_regex_pair_xor = 0

    return line


# ------------------------------------------------------------------------------------------------------------------
#   XOR calculating function
# ------------------------------------------------------------------------------------------------------------------
def calc_xor(param_1, param_2):
    tmp = ''
    if (CONST_NOT in param_1 or param_1 in CONST_CHAR) and (CONST_NOT in param_2 or param_2 in CONST_CHAR):
        tmp = param_1 + '^' + param_2
    elif CONST_NOT in param_1 or param_1 in CONST_CHAR:
        tmp = param_1
    elif CONST_NOT in param_2 or param_2 in CONST_CHAR:
        tmp = param_2
    else:
        if param_1 == CONST_TRUE and param_2 == CONST_TRUE:
            tmp = CONST_FALSE
        elif param_1 == CONST_FALSE and param_2 == CONST_TRUE:
            tmp = CONST_TRUE
        elif param_1 == CONST_TRUE and param_2 == CONST_FALSE:
            tmp = CONST_TRUE
        elif param_1 == CONST_FALSE and param_2 == CONST_FALSE:
            tmp = CONST_FALSE
    return tmp
