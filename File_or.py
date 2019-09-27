from Header import *


# ----------------------------------------------------------------------------------------
#   fonction de gestion OR
# ------------------------------------------------------------------------------------------------------------------

def operation_or(line, group):
    # boucle de toute les occurrence OR
    flag_regex_pair_or = 1
    while flag_regex_pair_or == 1:
        # creation d'une copie de la regle
        tmp_or_copy = line
        tuple_regex_pair_or = search_regex(group, CONST_REGEX_PAIR_OR)
        for n, pair_or in enumerate(tuple_regex_pair_or):
            param = recup_param(pair_or)
            rep = calc_or(param[0], param[1])
            line = line.replace(tuple_regex_pair_or[n], rep)
        if tmp_or_copy == line:
            flag_regex_pair_or = 0


# ------------------------------------------------------------------------------------------------------------------
#   fonction de calcul OR
# ------------------------------------------------------------------------------------------------------------------
def calc_or(param_1, param_2):
    tmp = ""
    if (CONST_NOT in param_1 or param_1 in CONST_CHAR) and (CONST_NOT in param_2 or param_2 in CONST_CHAR):
        tmp = CONST_FALSE
    elif CONST_NOT in param_1 or param_1 in CONST_CHAR:
        if param_2 == CONST_FALSE:
            tmp = param_1
        elif param_2 == CONST_TRUE:
            tmp = CONST_TRUE
    elif CONST_NOT in param_2 or param_2 in CONST_CHAR:
        if param_1 == CONST_FALSE:
            tmp = param_2
        elif param_1 == CONST_TRUE:
            tmp = CONST_TRUE
    else:
        if param_1 == CONST_TRUE and param_2 == CONST_TRUE:
            tmp = CONST_TRUE
        elif param_1 == CONST_FALSE and param_2 == CONST_TRUE:
            tmp = CONST_TRUE
        elif param_1 == CONST_TRUE and param_2 == CONST_FALSE:
            tmp = CONST_TRUE
        elif param_1 == CONST_FALSE and param_2 == CONST_FALSE:
            tmp = CONST_FALSE
    return tmp
