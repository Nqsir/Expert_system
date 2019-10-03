from Header.Header import *


# ------------------------------------------------------------------------------------------------------------------
#   Replacement function of negative value
# ------------------------------------------------------------------------------------------------------------------
def calc_neg(param_1, value, list_unknown):
    if value[param_1] != '':
        if value[param_1] == CONST_TRUE:
            tmp = CONST_TRUE
        else:
            tmp = CONST_FALSE
    else:
        tmp = param_1
        list_unknown.append(tmp)

    return tmp


# ------------------------------------------------------------------------------------------------------------------
#   Replacement function of positive value
# ------------------------------------------------------------------------------------------------------------------
def calc_pos(param_1, value, list_unknown):
    if value[param_1] != '':
        tmp = value[param_1]
    else:
        tmp = param_1
        list_unknown.append(tmp)

    return tmp
