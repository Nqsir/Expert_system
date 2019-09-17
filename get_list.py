from Errors import disp_errors_dict

CONST_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
OK = 0
def if_exist(list, element):
    for elem in list:
        if element == elem:
            return True
    return False


def simply_list(list):
    list_if = list[0]
    list_then = list[1]

    x = 0
    while x < len(list_then):
        y = x+1
        while y < len(list_then):
            if list_then[x] == list_then[y]:
                list_start = ["|"]
                list_if[x].append(list_start)
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
                        for o, elt in enumerate(list_if[x]):
                            line_search.insert(n + o, elt)
                        flag_next = 1
    return OK


def convert_to_only_one_then(list):
    list_if = list[0]
    list_then = list[1]
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


def to_list(list):
    tmp = []
    for elt in list:
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


def translat_to_list(list):
    list_if = []
    list_then = []
    for n, elt in enumerate(list):
        list_if.append(elt[0])
        list_then.append([x for x in elt[1] if x != '(' and x != ')'])
    list.clear()
    list.append(to_list(list_if))
    list.append(to_list(list_then))
    convert_to_only_one_then(list)
    errors = simply_list(list)
    return errors




#
# utilise une liste double en entrer : liste[[if],[then]]
#

#var = ["(A+!B+C|A)=>Z+(!V)", "(!G+!H)=>(A)+(Z)", "(A|J+S)=>Z"]
var = ["(A+(C|Y)+B+(C|D)+E)=>F", "(C+Z)=>F", "(G+H|I)=>C", "(J|K)=>H", "(K+(C|L))=>J"]
#var = ["(A)=>B", "(B)=>C", "(C)=>A"]

list_total = []

for elt in var:
    list_total.append(elt.split("=>"))

print("BEFORE :")
print("\tIF :")
for elt in list_total:
    print("\t\t", elt[0])
print("\tTHEN :")
for elt in list_total:
    print("\t\t", elt[1])


errors = translat_to_list(list_total)
if errors:
    disp_errors_dict(errors)


print("AFTER :")
print("\tIF :")
for elt in list_total[0]:
    print("\t\t", elt)
print("\tTHEN :")
for elt in list_total[1]:
    print("\t\t", elt)
