CONST_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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
    flag = 1
    while flag > 0:
        flag = 0
        x = -1
        for elem_A in list_then:
            x = x + 1
            y = -1
            for line in list_if:
                for n, elem_B in enumerate(line):
                    y = y + 1
                    if elem_B == elem_A[0]:
                        line.pop(n)
                        for o, elt in enumerate(list_if[x]):
                            line.insert(n + o, elt)
                        flag = flag + 1


def to_list(list_if):
    tmp = []
    for elt in list_if:
        list_tmp_if = []
        for n, char in enumerate(elt):
            list_tmp = []
            if n > 0 and (char in CONST_CHAR) and elt[n - 1] == '!':
                list_tmp.append('!'+elt[n])
            elif char != '!':
                list_tmp.append(elt[n])
            if len(list_tmp):
                list_tmp_if.append(list_tmp)
        tmp.append(list_tmp_if)
    return tmp


def convert_to_only_one_then(list):
    list_and = ["+"]
    for n, line in enumerate(list[1]):
        x = 0
        while x < len(line):
            if list_and == list[1][n][x]:
                list[0].append(list[0][n].copy())
                list_tmp = []
                list_tmp.append(list[1][n][x+1])
                list[1].append(list_tmp.copy())
                del list[1][n][x]
                del list[1][n][x]
                x = x - 1
            x = x + 1


def translat_to_list(list):
    list_if = []
    list_then = []
    for n, elt in enumerate(list):
        list_if.append(elt[0])
        list_then.append(elt[1])
    list.clear()
    list.append(to_list(list_if))
    list.append(to_list(list_then))
    convert_to_only_one_then(list)
    simply_list(list)


#
# utilise une liste double en entrer : liste[[if],[then]]
#


var = ["(A+!B+C)=>Z+!V", "(!G+!H)=>A+Z", "(A|J+S)=>Z"]

list_total = []

for elt in var:
    list_total.append(elt.split("=>"))

print("BEFOR :")
print("\tIF :")
for elt in list_total:
    print("\t\t", elt[0])
print("\tTHEN :")
for elt in list_total:
    print("\t\t", elt[1])

print("AFTER :")
translat_to_list(list_total)
print("\tIF :")
for elt in list_total[0]:
    print("\t\t", elt)
print("\tTHEN :")
for elt in list_total[1]:
    print("\t\t", elt)