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
