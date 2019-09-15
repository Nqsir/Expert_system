CONST_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

var = ["(!A+B+!C)=>Z", "(D+(!E+F))=>A", "(D|F)=>C", "(G+H)=>Z", "(F)=>D", "(A|J+S)=>Z"]

list_total = []
list_if = []
list_then = []

for elt in var:
    list_total.append(elt.split("=>"))

for elt in list_total:
    print(elt)

for elt in list_total:
    list_tmp_if = []

    for n, char in enumerate(elt[0]):
        list_tmp = []
        if n > 0 and (char in CONST_CHAR) and elt[0][n-1] == '!':
            list_tmp.append('!')
            list_tmp.append(elt[0][n])
        elif char != '!':
            list_tmp.append(elt[0][n])
        if len(list_tmp):
            list_tmp_if.append(list_tmp)
    list_if.append(list_tmp_if)

    list_tmp_2 = []
    if '!' in elt[1]:
        list_tmp_2.append('!')
    else:
        list_tmp_2.append('')
    list_tmp_2.append(elt[1].replace('!', ''))
    list_then.append(list_tmp_2)

for elt in list_then:
    print(elt)


for elt in list_if:
    print(elt)