from Header.Header import *

from Modules.File_useful_function import simplify_parentheses


def reverse_if_and_then(list_t):
    # list_t copying loop
    list_tmp = []
    for n, zone in enumerate(list_t):
        list_tmp.append([])
        for o, line in enumerate(zone):
            list_tmp[n].append([])
            for p, element in enumerate(line):
                list_tmp[n][o].append([list_t[n][o][p][0]])

    # Pointing on list_if and list_then
    list_not_if = list_tmp[0]
    list_not_then = list_tmp[1]

    # Modification loop for list_not_if
    for n, line in enumerate(list_not_if):
        for o, element in enumerate(line):
            if element[0] in CONST_CHAR:
                element[0] = "!"+element[0]
            elif "!" in element[0]:
                element[0] = element[0][1]
            elif "+" in element[0]:
                element[0] = "|"
            elif "|" in element[0]:
                element[0] = "+"

    # Modification loop for list_not_then
    for n, line in enumerate(list_not_then):
        for o, element in enumerate(line):
            if element[0] in CONST_CHAR:
                element[0] = "!"+element[0]
            elif "!" in element[0]:
                element[0] = element[0][1]

    # Extending lists with list_not
    list_t[0].extend(list_not_if)
    list_t[1].extend(list_not_then)


def list_to_str(list_):
    # Conversion loop from list to str
    for n, elt in enumerate(list_):
        string = re.sub(r'''\[*\]*\'*\s*,*''', '', str(elt))
        while True:
            string = re.sub(r'''(\()(!?[A-Z])(\))''', r'\2', string)
            if not re.findall(r'''(\(!?[A-Z]\))''', string):
                break

        list_[n] = [simplify_parentheses(string)]


def if_exist(list_, element):
    for elem in list_:
        if element == elem:
            return True

    return False


def simply_list(list_):
    list_if = list_[0]
    list_then = list_[1]

    # Grouping loop multiple rules
    x = 0
    while x < len(list_then):
        y = x+1
        while y < len(list_then):
            if list_then[x] == list_then[y]:
                list_if[x].append(["|"])
                list_if[x].extend(list_if[y])
                del list_if[y]
                del list_then[y]
                y = y-1
            y = y + 1
        x = x + 1

    # Looking for relation between rules, checking infinite loop and insertion
    x = 0
    flag_next = 1
    while flag_next > 0:
        flag_next = 0
        x = -1
        for m, elem_search in enumerate(list_then):
            x = x + 1
            for y, line_search in enumerate(list_if):
                for n, elem in enumerate(line_search):
                    if elem == elem_search[0]:
                        if if_exist(list_if[m], list_then[y][0]):
                            return 'loop', list_then[y][0][0]
                        line_search.pop(n)
                        line_search.insert(n, ["("])
                        line_search.insert(n + 1, [")"])
                        for o, elt in enumerate(list_if[x]):
                            line_search.insert(n + 1 + o, elt)
                        flag_next = 1

    list_to_str(list_[0])
    list_to_str(list_[1])

    return OK


def convert_to_only_one_then(list_):
    list_if = list_[0]
    list_then = list_[1]
    list_and = ["+"]

    for n, line in enumerate(list_then):
        x = 0
        while x < len(line):
            if list_and == list_then[n][x]:
                list_tmp = []
                list_if.append(list_if[n].copy())
                list_tmp.append(list_then[n][x+1])
                list_then.append(list_tmp.copy())
                del list_then[n][x]
                del list_then[n][x]
                x = x - 1
            x = x + 1


def to_list(list_):
    tmp = []
    for elt in list_:
        list_tmp_var = []
        for n, char in enumerate(elt):
            list_tmp = []
            if n > 0 and (char in CONST_CHAR) and elt[n - 1] == '!':
                list_tmp.append('!' + elt[n])
            elif char != '!':
                list_tmp.append(elt[n])
            if len(list_tmp):
                list_tmp_var.append(list_tmp)
        tmp.append(list_tmp_var)

    return tmp


def translat_to_list(list_total, _logger):
    list_if = []
    list_then = []
    for n, elt in enumerate(list_total):
        list_if.append(elt[0])
        list_then.append([x for x in elt[1] if x != '(' and x != ')'])
    list_total.clear()
    list_total.append(to_list(list_if))
    list_total.append(to_list(list_then))
    convert_to_only_one_then(list_total)
    reverse_if_and_then(list_total)

    rep = simply_list(list_total)

    # -------------------------------- START Only prints ------------------------------------------
    max_l = len(max([_[0] for _ in list_total[0]], key=len))

    _logger.debug('\n=========== EXTENDED RULES =========== \n'
                  f'{"IF":{max_l + 5}s}\t{"THEN"}')
    _logger.debug(f'{"-" * max_l:{max_l + 5}s}\t{"------"}')
    for n in range(len(list_total[0])):
        str_1 = re.sub(r'''\[*\]*\'*\s*,*''', '', str(list_total[0][n]))
        str_2 = re.sub(r'''\[*\]*\'*\s*,*''', '', str(list_total[1][n]))
        _logger.debug(f'{str_1:{max_l + 5}s}\t{str_2:s}')
    _logger.debug('\n')
    # -------------------------------- END Only prints ------------------------------------------

    return rep

