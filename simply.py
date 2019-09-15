

One = [['a', 'b'], ['c', 'd']]

Two = [['e', 'f'], ['a', 'b']]

for O in One:

    print(f'{O} is in Two = {O in Two}')



var = ["(A+B+C)=>Z", "(D+(E+F))=>A", "(D|F)=>C", "(G+H)=>Z", "(F)=>D", "(A|J+S)=>Z"]

list_total = []

list_if = []
list_then = []

for elt in var:
    print(elt)
for elt in var:
    list_total.append(elt.split("=>"))

for elt in list_total:
    list_if.append(elt[0])
    list_then.append(elt[1])


x = 0
while x < len(list_then):
    y = x
    while y < len(list_then):
        if x != y:
            trouve = list_then[y].find(list_then[x])
            trouve_2 = list_then[y].find("!"+list_then[x])
            if trouve > -1 and trouve_2 == -1:
                tmp = list_if[x] + "|(" + list_if[y] + ")"
                list_if[x] = tmp
                del list_then[y]
                del list_if[y]
                y = y-1
        y = y + 1
    x = x + 1

modif = 1
while modif > 0:
    modif = 0
    x = -1
    for elt in list_then:
        x = x+1
        y = -1
        for ligne in list_if:
            y = y+1
            trouve = ligne.find(elt)
            if trouve > -1:
                tmp = ligne.replace(elt, list_if[x])
                list_if[y] = tmp
                modif = modif + 1


x = 0
for elt in list_then:
    print(elt, " = ", list_if[x])
    x = x+1