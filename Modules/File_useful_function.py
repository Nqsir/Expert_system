from Header.Header import *


# ------------------------------------------------------------------------------------------------------------------
#   Looking for regex in string function
# ------------------------------------------------------------------------------------------------------------------
def search_regex(string, regex):
    tuple_regex = list(set(re.findall(regex, string)))
    return tuple_regex


# ------------------------------------------------------------------------------------------------------------------
#   Getting parameters function
# ------------------------------------------------------------------------------------------------------------------
def get_param(pair):
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
#   Getting value function
# ------------------------------------------------------------------------------------------------------------------
def get_val(val):
    val = re.sub(r'''\(*\)*''', '', val)
    return val


# ------------------------------------------------------------------------------------------------------------------
#   Deleting parentheses function
# ------------------------------------------------------------------------------------------------------------------
def simplify_parentheses(rules):
    list_parentheses = []
    size_parentheses = 0
    pile = []

    for n, elem in enumerate(rules):
        if elem == '(':
            pile.insert(0, n)
        if elem == ')':
            list_parentheses.append([pile[0], n])
            size_parentheses += 1
            pile.pop(0)

    flag_run = 1
    index = 0
    tmp = list(rules)
    while flag_run == 1:
        flag = 0
        if index + 1 < size_parentheses:
            if (list_parentheses[index + 1][0] == list_parentheses[index][0] + 1
                or list_parentheses[index + 1][0] == list_parentheses[index][0] - 1) \
                    and (list_parentheses[index + 1][1] == list_parentheses[index][1] + 1
                         or list_parentheses[index + 1][1] == list_parentheses[index][1] - 1):
                name_a = list_parentheses[index][0]
                name_b = list_parentheses[index][1]
                list_parentheses.pop(index)
                size_parentheses -= 1
                tmp[name_a] = " "
                tmp[name_b] = ' '
                index = 0
                flag = 1
        if index >= size_parentheses:
            flag_run = 0
        if flag == 0:
            index += 1

    tmp = "".join(tmp)
    tmp = tmp.replace(' ', '')
    return tmp
