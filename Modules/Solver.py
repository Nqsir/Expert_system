from Header.Header import *

from Modules.File_useful_function import search_regex
from Modules.File_calc_value import calc_neg, calc_pos
from Modules.File_unitary import operation_unitary
from Modules.File_and import operation_and
from Modules.File_or import operation_or
from Modules.File_xor import operation_xor


def solver(list_total, list_fact, list_query):
    list_total = list_total
    list_if = list_total[0]
    list_then = list_total[1]
    list_fact = list_fact
    list_query = list_query
    list_unknown = []
    value = {}
    init_value(value, list_then, list_fact)
    for n, query in enumerate(list_query):
        if query in list_then:
            rep = [query[0].replace('!', '')]
            name_a = rep
            name_b = [f'!{rep[0]}']
            value[name_a[0]] = order(list_if[list_then.index(name_a)][0], list_unknown, value)
            value[name_b[0]] = order(list_if[list_then.index(name_b)][0], list_unknown, value)
    for m, query in enumerate(list_query):
        name_a = query
        name_b = list([f'!{query[0]}'])
        if value[name_a[0]] == value[name_b[0]]:
            print(f'\x1b[1;30;42m{name_a} is undetermined \x1b[0m')
        else:
            print(f'\x1b[1;30;42m{query} is {"True" if value[query[0]] == "1" else "False"} \x1b[0m')


# ------------------------------------------------------------------------------------------------------------------
#   Initialises dictionary
# ------------------------------------------------------------------------------------------------------------------
def init_value(value, list_then, list_fact):
    for char in CONST_CHAR:
        value[char] = CONST_FALSE
        value[f'!{char}'] = CONST_TRUE
    for n, then in enumerate(list_then):
        rep = then[0].replace('!', '')
        name_a = rep
        name_b = f'!{rep}'
        value[f'{name_a}'] = ''
        value[f'{name_b}'] = ''
    for n, fact in enumerate(list_fact):
        value[fact[0]] = CONST_TRUE
        value[f'!{fact[0]}'] = CONST_FALSE


# ------------------------------------------------------------------------------------------------------------------
#   Solving method
# ------------------------------------------------------------------------------------------------------------------
def order(line, list_unknown, value):
    list_unknown.clear()
    line = f'({line})'

    # Look for the pattern depending on the regex
    tuple_regex_unitary = search_regex(line, CONST_REGEX_UNITARY)

    # Replacement loop letter to value (0, 1)
    for n, element_unitary in enumerate(tuple_regex_unitary):
        if CONST_NOT in element_unitary:
            tmp_str = calc_neg(element_unitary, value, list_unknown)
        else:
            tmp_str = calc_pos(element_unitary, value, list_unknown)
        if element_unitary == tmp_str:
            pass
        else:
            line = line.replace(element_unitary, tmp_str)

    # Master solving loop
    flag_run = 1
    while flag_run == 1:
        line_copy = line

        # Look for the pattern depending on the group regex
        tuple_regex_group = search_regex(line, CONST_REGEX_GROUP)

        # Group loop
        flag_regex_group = 1
        while flag_regex_group == 1:
            group_copy = line
            for m, group in enumerate(tuple_regex_group):
                line = operation_unitary(line, group)
                line = operation_and(line, group)
                line = operation_or(line, group)
                line = operation_xor(line, group)

            # Stopping condition (group loop)
            if group_copy == line:
                flag_regex_group = 0

        # Stopping condition (master loop)
        if line_copy == line:
            flag_run = 0

    return line










