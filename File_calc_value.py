from Header import *


# ------------------------------------------------------------------------------------------------------------------
#   fonction de remplacement de la valeur negative
# ------------------------------------------------------------------------------------------------------------------
def calc_neg(self, param_1):
    if self.value[param_1] != '':
        if self.value[param_1] == CONST_TRUE:
            tmp = CONST_TRUE
        else:
            tmp = CONST_FALSE
    else:
        tmp = param_1
        self.list_unknown.append(tmp)
    return tmp


# ------------------------------------------------------------------------------------------------------------------
#   fonction de remplacement de la valeur positive
# ------------------------------------------------------------------------------------------------------------------
def calc_pos(self, param_1):
    if self.value[param_1] != '':
        tmp = self.value[param_1]
    else:
        tmp = param_1
        self.list_unknown.append(tmp)
    return tmp
