import re

CONST_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
OK = 0


def list_to_str(list_):
    for n, elt in enumerate(list_):
        string = re.sub(r'''\[*\]*\'*\s*,*''', '', str(elt))
        while True:
            string = re.sub(r'''(\()(!?[A-Z])(\))''', r'\2', string)
            if not re.findall(r'''(\(!?[A-Z]\))''', string):
                break
        list_[n] = [string]


def if_exist(list_, element):
    for elem in list_:
        if element == elem:
            return True
    return False


def simply_list(list_):
    list_if = list_[0]
    list_then = list_[1]

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

    x = 0
    flag_next = 1
    while flag_next > 0:
        flag_next = 0
        x = -1
        for m, elem_search in enumerate(list_then):
            x = x + 1
            for y, line_search in enumerate(list_if):
                for n, elem in enumerate(line_search):
                    if if_exist(list_if[y-1], list_then[y-1][0]):
                        msg = elem_search[0][0]
                        return 'loop', msg
                    if elem == elem_search[0]:
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


def translat_to_list(list_total):
    list_if = []
    list_then = []
    for n, elt in enumerate(list_total):
        list_if.append(elt[0])
        list_then.append([x for x in elt[1] if x != '(' and x != ')'])
    list_total.clear()
    list_total.append(to_list(list_if))
    list_total.append(to_list(list_then))
    convert_to_only_one_then(list_total)

    # Only Prints
    max_l = len(max([_ for _ in list_total[0]], key=len))
    print('\nrules = \n'
          f'{"IF":{max_l + 5}s}\t{"THEN"}')
    print(f'{"-------":{max_l + 5}s}\t{"-------"}')
    for n in range(len(list_total[0])):
        str_1 = re.sub(r'''\[*\]*\'*\s*,*''', '', str(list_total[0][n]))
        str_2 = re.sub(r'''\[*\]*\'*\s*,*''', '', str(list_total[1][n]))
        print(f'{str_1:{max_l + 5}s}\t{str_2:s}')
    print('\n')

    errors = simply_list(list_total)
    return errors


