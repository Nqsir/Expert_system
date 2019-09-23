CONST_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CONST_NOT = "!"
CONST_REGEX_UNITARY = ""
CONST_REGEX_GROUP = ""
CONST_REGEX_PAIR_AND = ""
CONST_REGEX_PAIR_OR = ""
CONST_REGEX_PAIR_XOR = ""


class Resolver:
    def __init__(self, list_string, list_fact):
        self.list_string = list_string

    # ------------------------------------------------------------------------------------------------------------------
    #   methode resolution
    # ------------------------------------------------------------------------------------------------------------------
    def order(self, line):
        memory_string_inc = ""

        # recherche pattern avec la regex unitaire
        tuple_regex_unitary = self.search_regex(line, CONST_REGEX_UNITARY)

        # boucle remplacement des lettre par leur valeur
        for n, element_unitary in enumerate(tuple_regex_unitary):
            if CONST_NOT in element_unitary:
                tmp_str = self.calc_neg(element_unitary)
            else:
                tmp_str = self.calc_pos(element_unitary)
            if element_unitary == tmp_str:
                break
            else:
                line.replace(element_unitary, tmp_str)

        # boucle principale de resolution
        flag_run = 1
        while flag_run == 1:
            line_copy = line.copy()

            # recherche pattern avec la reg regex de groupe
            tuple_regex_groupe = self.search_regex(line, CONST_REGEX_GROUP)

            # boucle des goupe
            flag_regex_group = 1
            while flag_regex_group == 1:
                group_copy = line.copy()
                for m, group in enumerate(tuple_regex_groupe):

                    # boucle de toute les occurrence AND
                    flag_regex_pair_and = 1
                    while flag_regex_pair_and == 1:
                        # creation d'une copie de la regle
                        tmp_and_copy = line.copy()
                        # recherche pattern avec la regex paire and
                        tuple_regex_pair_and = self.search_regex(group[m], CONST_REGEX_PAIR_AND)
                        for n, pair_and in enumerate(tuple_regex_pair_and):
                            # fonction qui recupere que les 2 param
                            # recup_param(pair_and, param_1, param_2)
                            param_1 = ""
                            param_2 = ""
                            rep = self.calc_and(param_1, param_2)
                            str(line).replace(tuple_regex_pair_and[n], rep)
                        if tmp_and_copy == line:
                            flag_regex_pair_and = 0

                    # boucle de toute les occurrence OR
                    flag_regex_pair_or = 1
                    while flag_regex_pair_or == 1:
                        # creation d'une copie de la regle
                        tmp_or_copy = line.copy()
                        # recherche pattern avec la regex paire or
                        tuple_regex_pair_or = self.search_regex(group[m], CONST_REGEX_PAIR_OR)
                        for n, pair_or in enumerate(tuple_regex_pair_or):
                            # fonction qui recupere que les 2 param
                            # recup_param(pair_or, param_1, param_2)
                            param_1 = ""
                            param_2 = ""
                            rep = self.calc_or(param_1, param_2)
                            str(line).replace(tuple_regex_pair_or[n], rep)
                        if tmp_or_copy == line:
                            flag_regex_pair_or = 0

                    # boucle de toute les occurrence XOR
                    flag_regex_pair_xor = 1
                    while flag_regex_pair_xor == 1:
                        # creation d'une copie de la regle
                        tmp_line_copy = line.copy()
                        # recherche pattern avec la regex paire xor
                        tuple_regex_pair_xor = self.search_regex(group[m], CONST_REGEX_PAIR_XOR)
                        for n, pair_or in enumerate(tuple_regex_pair_xor):
                            # fonction qui recupere que les 2 param
                            # recup_param(pair_or, param_1, param_2)
                            param_1 = ""
                            param_2 = ""
                            rep = self.calc_xor(param_1, param_2)
                            str(line).replace(tuple_regex_pair_xor[n], rep)
                        if tmp_line_copy == line:
                            flag_regex_pair_xor = 0
                if line_copy == line:
                    flag_regex_group = 0

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de calcul AND
    # ------------------------------------------------------------------------------------------------------------------
    def calc_and(self, param_1, param_2):
        tmp = ""
        if (CONST_NOT in param_1 or param_1 in CONST_CHAR) and (CONST_NOT in param_2 or param_2 in CONST_CHAR):
            tmp = "0"
            # memoriser tmp = param_1 + "+" + param_2
        elif CONST_NOT in param_1 or param_1 in CONST_CHAR:
            if param_2 == "0":
                tmp = "0"
            elif param_2 == "1":
                tmp = param_1
        elif CONST_NOT in param_2 or param_2 in CONST_CHAR:
            if param_1 == "0":
                tmp = "0"
            elif param_1 == "1":
                tmp = param_2
        else:
            if param_1 == "1" and param_2 == "1":
                tmp = "1"
            elif param_1 == "0" and param_2 == "1":
                tmp = "0"
            elif param_1 == "1" and param_2 == "0":
                tmp = "0"
            elif param_1 == "0" and param_2 == "0":
                tmp = "0"
        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de calcul OR
    # ------------------------------------------------------------------------------------------------------------------
    def calc_or(self, param_1, param_2):
        tmp = ""
        if (CONST_NOT in param_1 or param_1 in CONST_CHAR) and (CONST_NOT in param_2 or param_2 in CONST_CHAR):
            tmp = "0"
            # memoriser tmp = param_1 + "|" + param_2
        elif CONST_NOT in param_1 or param_1 in CONST_CHAR:
            if param_2 == "0":
                tmp = param_1
            elif param_2 == "1":
                tmp = "1"
        elif CONST_NOT in param_2 or param_2 in CONST_CHAR:
            if param_1 == "0":
                tmp = param_2
            elif param_1 == "1":
                tmp = "1"
        else:
            if param_1 == "1" and param_2 == "1":
                tmp = "1"
            elif param_1 == "0" and param_2 == "1":
                tmp = "1"
            elif param_1 == "1" and param_2 == "0":
                tmp = "1"
            elif param_1 == "0" and param_2 == "0":
                tmp = "0"
        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de calcul XOR
    # ------------------------------------------------------------------------------------------------------------------
    def calc_xor(self, param_1, param_2):
        tmp = ""
        if (CONST_NOT in param_1 or param_1 in CONST_CHAR) or (CONST_NOT in param_2 or param_2 in CONST_CHAR):
            tmp = "0"
            # memoriser tmp = param_1 + "^" + param_2
        else:
            if param_1 == "1" and param_2 == "1":
                tmp = "0"
            elif param_1 == "0" and param_2 == "1":
                tmp = "1"
            elif param_1 == "1" and param_2 == "0":
                tmp = "1"
            elif param_1 == "0" and param_2 == "0":
                tmp = "0"
        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de remplacement de la valeur negative
    # ------------------------------------------------------------------------------------------------------------------
    def calc_neg(self, param_1):
        tmp = ""
        # remplace la letre par l'inverse de sa valeur si elle est connu, sinon laisse comme c'est
        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de remplacement de la valeur positive
    # ------------------------------------------------------------------------------------------------------------------
    def calc_pos(self, param_1):
        tmp = ""
        # remplace la letre par sa valeur si elle est connu, sinon laisse comme c'est
        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de recherche regex dans une string
    # ------------------------------------------------------------------------------------------------------------------
    def search_regex(self, string, regex):

        tuple_regex = list(set())
        return tuple_regex
