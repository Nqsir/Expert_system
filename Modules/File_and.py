from Header.Header import *

from Modules.File_useful_function import search_regex, get_param


# ------------------------------------------------------------------------------------------------------------------
#   AND handling function
# ------------------------------------------------------------------------------------------------------------------
def operation_and(line, group):
    # AND occurrences checking loop
    flag_regex_pair_and = 1
    while flag_regex_pair_and == 1:
        # Rule copy
        tmp_and_copy = line
        tuple_regex_pair_and = search_regex(group, CONST_REGEX_PAIR_AND)
        for n, pair_and in enumerate(tuple_regex_pair_and):
            param = get_param(pair_and)
            rep = calc_and(param[0], param[1])
            line = line.replace(tuple_regex_pair_and[n], rep)
        if tmp_and_copy == line:
            flag_regex_pair_and = 0

    return line


# ------------------------------------------------------------------------------------------------------------------
#   AND calculating function
# ------------------------------------------------------------------------------------------------------------------
def calc_and(param_1, param_2):
    tmp = ''
    if (CONST_NOT in param_1 or param_1 in CONST_CHAR) and (CONST_NOT in param_2 or param_2 in CONST_CHAR):
        tmp = CONST_FALSE
    elif CONST_NOT in param_1 or param_1 in CONST_CHAR:
        if param_2 == CONST_FALSE:
            tmp = CONST_FALSE
        elif param_2 == CONST_TRUE:
            tmp = param_1
    elif CONST_NOT in param_2 or param_2 in CONST_CHAR:
        if param_1 == CONST_FALSE:
            tmp = CONST_FALSE
        elif param_1 == CONST_TRUE:
            tmp = param_2
    else:
        if param_1 == CONST_TRUE and param_2 == CONST_TRUE:
            tmp = CONST_TRUE
        elif param_1 == CONST_FALSE and param_2 == CONST_TRUE:
            tmp = CONST_FALSE
        elif param_1 == CONST_TRUE and param_2 == CONST_FALSE:
            tmp = CONST_FALSE
        elif param_1 == CONST_FALSE and param_2 == CONST_FALSE:
            tmp = CONST_FALSE
    return tmp
