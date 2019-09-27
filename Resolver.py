from Header import *

from File_useful_function import search_regex
from File_calc_value import calc_neg, calc_pos
from File_unitary import operation_unitary
from File_and import operation_and
from File_or import operation_or
from File_xor import operation_xor


def resolver(list_total, list_fact, list_query):
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
            pos = list_then.index(query)
            value[query[0]] = order(list_if[pos][0], list_unknown, value)

    print(f' value after : {value}')
    for m, query in enumerate(list_query):
        print(f' for {query} the reponse is {value[query[0]]}')


# ------------------------------------------------------------------------------------------------------------------
#   methode initialisation des valeurs dictionnaire
# ------------------------------------------------------------------------------------------------------------------
def init_value(value, list_then, list_fact):
    for char in CONST_CHAR:
        value[char] = CONST_FALSE
        value[f'!{char}'] = CONST_TRUE
    for n, then in enumerate(list_then):
        value[then[0]] = ''
    for n, fact in enumerate(list_fact):
        value[fact[0]] = CONST_TRUE
        value[f'!{fact[0]}'] = CONST_FALSE
    print(f'self.value = {value}')


# ------------------------------------------------------------------------------------------------------------------
#   methode resolution
# ------------------------------------------------------------------------------------------------------------------
def order(line, list_unknown, value):
    list_unknown.clear()
    line = f'({line})'

    # recherche pattern avec la regex unitaire
    tuple_regex_unitary = search_regex(line, CONST_REGEX_UNITARY)

    # boucle remplacement des lettre par leur valeur
    for n, element_unitary in enumerate(tuple_regex_unitary):
        if CONST_NOT in element_unitary:
            tmp_str = calc_neg(element_unitary, value, list_unknown)
        else:
            tmp_str = calc_pos(element_unitary, value, list_unknown)
        if element_unitary == tmp_str:
            pass
        else:
            line = line.replace(element_unitary, tmp_str)

    # boucle principale de resolution
    flag_run = 1
    print(f'line = {line}')
    while flag_run == 1:
        line_copy = line

        # recherche pattern avec la reg regex de groupe
        tuple_regex_group = search_regex(line, CONST_REGEX_GROUP)
        print(f'groupe = {tuple_regex_group}')
        # boucle des goupe
        flag_regex_group = 1
        while flag_regex_group == 1:
            group_copy = line
            for m, group in enumerate(tuple_regex_group):

                line = operation_unitary(line, group)

                print(f'line = {line}')

                line = operation_and(line, group)

                print(f'line = {line}')

                line = operation_or(line, group)

                print(f'line = {line}')

                line = operation_xor(line, group)

                print(f'line = {line}')

            # condition d'arret de la boucle des groupe
            if group_copy == line:
                flag_regex_group = 0

        # condition d'arret de la boucle principale
        if line_copy == line:
            flag_run = 0
    print(f'line = {line}')
    return line










