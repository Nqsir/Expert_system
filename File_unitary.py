from Header import *

from File_useful_function import search_regex
from File_useful_function import recup_val

# ------------------------------------------------------------------------------------------------------------------
#   fonction de gestion unitaire
# ------------------------------------------------------------------------------------------------------------------
def operation_unitary(line, group):
    # boucle de toute les occurrence unitaire
    flag_regex_unitary = 1
    while flag_regex_unitary == 1:
        # creation d'une copie de la regle
        tmp_unitary_copy = line
        tuple_regex_unity = search_regex(group, CONST_REGEX_UNITARY_PARENTHESES)
        for n, unity in enumerate(tuple_regex_unity):
            param = recup_val(unity)
            line = line.replace(tuple_regex_unity[n], param)
        if tmp_unitary_copy == line:
            flag_regex_unitary = 0

    return line
