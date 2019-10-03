from Header.Header import *

from Modules.File_useful_function import search_regex
from Modules.File_useful_function import get_val


# ------------------------------------------------------------------------------------------------------------------
#   Unitary handling function
# ------------------------------------------------------------------------------------------------------------------
def operation_unitary(line, group):
    # Unitary occurrences checking loop
    flag_regex_unitary = 1
    while flag_regex_unitary == 1:
        # Rule copy
        tmp_unitary_copy = line
        tuple_regex_unity = search_regex(group, CONST_REGEX_UNITARY_PARENTHESES)
        for n, unity in enumerate(tuple_regex_unity):
            param = get_val(unity)
            line = line.replace(tuple_regex_unity[n], param)
        if tmp_unitary_copy == line:
            flag_regex_unitary = 0

    return line
