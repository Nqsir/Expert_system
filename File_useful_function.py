import time

from Header import *

# ------------------------------------------------------------------------------------------------------------------
#   fonction de recherche regex dans une string
# ------------------------------------------------------------------------------------------------------------------

def search_regex(string, regex):
    tuple_regex = list(set(re.findall(regex, string)))
    return tuple_regex


# ------------------------------------------------------------------------------------------------------------------
#   fonction de recuperation des parametre
# ------------------------------------------------------------------------------------------------------------------
def recup_param(pair):
    pair = pair.replace('(', '').replace(')', '')
    if CONST_AND in pair:
        char = CONST_AND
    elif CONST_OR in pair:
        char = CONST_OR
    elif CONST_XOR in pair:
        char = CONST_XOR
    else:
        char = ""
    rep = pair.split(char)
    return rep


# ------------------------------------------------------------------------------------------------------------------
#   fonction de recuperation valeur
# ------------------------------------------------------------------------------------------------------------------
def recup_val(val):
    val = re.sub(r'''\(*\)*''', '', val)
    return val


# ------------------------------------------------------------------------------------------------------------------
#   fonction de suppression parenthèse
# ------------------------------------------------------------------------------------------------------------------
def simply_bracket(rules):
    list_bracket = []
    size_bracket = 0
    pile = []

    for n, elem in enumerate(rules):
        if elem == '(':
            pile.insert(0, n)
        if elem == ')':
            list_bracket.append([pile[0], n])
            size_bracket += 1
            pile.pop(0)

    flag_run = 1
    index = 0
    tmp = list(rules)
    while flag_run == 1:
        flag = 0
        if index + 1 < size_bracket:
            if (list_bracket[index + 1][0] == list_bracket[index][0] + 1 or list_bracket[index + 1][0] == list_bracket[index][0] - 1) and (list_bracket[index + 1][1] == list_bracket[index][1] + 1 or list_bracket[index + 1][1] == list_bracket[index][1] - 1):
                name_A = list_bracket[index][0]
                name_B = list_bracket[index][1]
                list_bracket.pop(index)
                size_bracket -= 1
                tmp[name_A] = " "
                tmp[name_B] = ' '
                index = 0
                flag = 1
        if index >= size_bracket:
            flag_run = 0
        if flag == 0:
            index += 1

    tmp = "".join(tmp)
    tmp = tmp.replace(' ', '')
    return tmp
