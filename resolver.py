import re

CONST_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

CONST_NOT = '!'
CONST_AND = '+'
CONST_OR = '|'
CONST_XOR = '^'

CONST_TRUE = '1'
CONST_FALSE = '0'

CONST_REGEX_UNITARY = r'(!?[A-Z01])'  # regex selection single value
CONST_REGEX_UNITARY_PARENTHESES = r'(\(!?[A-Z01]\))'  # regex selection single value with parentheses
CONST_REGEX_GROUP = r'(\([!A-Z01\+\|\^]+\))'  # regex selection group
CONST_REGEX_PAIR_AND = r'(!?[A-Z01]\+!?[A-Z01])'  # regex and
CONST_REGEX_PAIR_OR = r'(!?[A-Z01]\|!?[A-Z01])'  # regex or
CONST_REGEX_PAIR_XOR = r'(!?[A-Z01]\^!?[A-Z01])'  # regex xor


class Resolver:
    def __init__(self, list_total, list_fact, list_query):
        self.list_total = list_total
        self.list_if = list_total[0]
        self.list_then = list_total[1]
        self.list_fact = list_fact
        self.list_query = list_query
        self.list_unknown = []
        self.value = {}
        self.init_value()
        for n, query in enumerate(self.list_query):
            print(f'-----{query}-----')
            if query in self.list_then:
                pos = self.list_then.index(query)
                self.value[query[0]] = self.order(self.list_if[pos][0])

        for m, query in enumerate(self.list_query):
            print(f' for {query} the reponse is {self.value[query[0]]}')


    # ------------------------------------------------------------------------------------------------------------------
    #   methode initialisation des valeurs dictionnaire
    # ------------------------------------------------------------------------------------------------------------------
    def init_value(self):
        for char in CONST_CHAR:
            self.value[char] = CONST_FALSE
            self.value[f'!{char}'] = CONST_TRUE
        for n, then in enumerate(self.list_then):
            self.value[then[0]] = ''
        for n, fact in enumerate(self.list_fact):
            self.value[fact[0]] = CONST_TRUE
            self.value[f'!{fact[0]}'] = CONST_FALSE

        print(f'self.value = {self.value}')

    # ------------------------------------------------------------------------------------------------------------------
    #   methode resolution
    # ------------------------------------------------------------------------------------------------------------------
    def order(self, line):
        self.list_unknown.clear()
        line = f'({line})'

        # recherche pattern avec la regex unitaire
        tuple_regex_unitary = self.search_regex(line, CONST_REGEX_UNITARY)
        # boucle remplacement des lettre par leur valeur
        for n, element_unitary in enumerate(tuple_regex_unitary):
            if CONST_NOT in element_unitary:
                tmp_str = self.calc_neg(element_unitary)
            else:
                tmp_str = self.calc_pos(element_unitary)
            if element_unitary == tmp_str:
                pass
            else:
                line = line.replace(element_unitary, tmp_str)
        # boucle principale de resolution
        flag_run = 1
        print(f'line = {line}')
        while flag_run == 1:
            line_copy = line

            # recherche pattern avec la reg regex de groupe
            tuple_regex_group = self.search_regex(line, CONST_REGEX_GROUP)
            print(f'groupe = {tuple_regex_group}')
            # boucle des goupe
            flag_regex_group = 1
            while flag_regex_group == 1:
                group_copy = line
                for m, group in enumerate(tuple_regex_group):

                    # boucle de toute les occurrence unitaire
                    flag_regex_unitary = 1
                    while flag_regex_unitary == 1:
                        # creation d'une copie de la regle
                        tmp_unitary_copy = line
                        tuple_regex_unity = self.search_regex(group, CONST_REGEX_UNITARY_PARENTHESES)
                        for n, unity in enumerate(tuple_regex_unity):
                            param = self.recup_val(unity)
                            line = line.replace(tuple_regex_unity[n], param)
                        if tmp_unitary_copy == line:
                            flag_regex_unitary = 0

                    print(f'line = {line}')

                    # boucle de toute les occurrence AND
                    flag_regex_pair_and = 1
                    while flag_regex_pair_and == 1:
                        # creation d'une copie de la regle
                        tmp_and_copy = line
                        tuple_regex_pair_and = self.search_regex(group, CONST_REGEX_PAIR_AND)
                        for n, pair_and in enumerate(tuple_regex_pair_and):
                            param = self.recup_param(pair_and)
                            rep = self.calc_and(param[0], param[1])
                            line = line.replace(tuple_regex_pair_and[n], rep)
                        if tmp_and_copy == line:
                            flag_regex_pair_and = 0

                    print(f'line = {line}')

                    # boucle de toute les occurrence OR
                    flag_regex_pair_or = 1
                    while flag_regex_pair_or == 1:
                        # creation d'une copie de la regle
                        tmp_or_copy = line
                        tuple_regex_pair_or = self.search_regex(group, CONST_REGEX_PAIR_OR)
                        for n, pair_or in enumerate(tuple_regex_pair_or):
                            param = self.recup_param(pair_or)
                            rep = self.calc_or(param[0], param[1])
                            line = line.replace(tuple_regex_pair_or[n], rep)
                        if tmp_or_copy == line:
                            flag_regex_pair_or = 0

                    print(f'line = {line}')

                    # boucle de toute les occurrence XOR
                    flag_regex_pair_xor = 1
                    while flag_regex_pair_xor == 1:
                        # creation d'une copie de la regle
                        tmp_xor_copy = line
                        tuple_regex_pair_xor = self.search_regex(group, CONST_REGEX_PAIR_XOR)
                        for n, pair_xor in enumerate(tuple_regex_pair_xor):
                            param = self.recup_param(pair_xor)
                            rep = self.calc_xor(param[0], param[1])
                            line = line.replace(tuple_regex_pair_xor[n], rep)
                        if tmp_xor_copy == line:
                            flag_regex_pair_xor = 0

                    print(f'line = {line}')

                # condition d'arret de la boucle des groupe
                if group_copy == line:
                    flag_regex_group = 0

            # condition d'arret de la boucle principale
            if line_copy == line:
                flag_run = 0
        print(f'line = {line}')
        return line

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de calcul AND
    # ------------------------------------------------------------------------------------------------------------------
    def calc_and(self, param_1, param_2):
        tmp = ""
        if (CONST_NOT in param_1 or param_1 in CONST_CHAR) and (CONST_NOT in param_2 or param_2 in CONST_CHAR):
            tmp = CONST_FALSE
        elif CONST_NOT in param_1 or param_1 in CONST_CHAR:
            if param_2 == CONST_FALSE:
                tmp = CONST_FALSE
            elif param_2 == CONST_TRUE:
                tmp = param_1
        elif CONST_NOT in param_2 or param_2 in CONST_CHAR:
            if param_1 == CONST_FALSE:
                tmp = CONST_FALSE
            elif param_1 == CONST_TRUE:
                tmp = param_2
        else:
            if param_1 == CONST_TRUE and param_2 == CONST_TRUE:
                tmp = CONST_TRUE
            elif param_1 == CONST_FALSE and param_2 == CONST_TRUE:
                tmp = CONST_FALSE
            elif param_1 == CONST_TRUE and param_2 == CONST_FALSE:
                tmp = CONST_FALSE
            elif param_1 == CONST_FALSE and param_2 == CONST_FALSE:
                tmp = CONST_FALSE
        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de calcul OR
    # ------------------------------------------------------------------------------------------------------------------
    def calc_or(self, param_1, param_2):
        tmp = ""
        if (CONST_NOT in param_1 or param_1 in CONST_CHAR) and (CONST_NOT in param_2 or param_2 in CONST_CHAR):
            tmp = CONST_FALSE
        elif CONST_NOT in param_1 or param_1 in CONST_CHAR:
            if param_2 == CONST_FALSE:
                tmp = param_1
            elif param_2 == CONST_TRUE:
                tmp = CONST_TRUE
        elif CONST_NOT in param_2 or param_2 in CONST_CHAR:
            if param_1 == CONST_FALSE:
                tmp = param_2
            elif param_1 == CONST_TRUE:
                tmp = CONST_TRUE
        else:
            if param_1 == CONST_TRUE and param_2 == CONST_TRUE:
                tmp = CONST_TRUE
            elif param_1 == CONST_FALSE and param_2 == CONST_TRUE:
                tmp = CONST_TRUE
            elif param_1 == CONST_TRUE and param_2 == CONST_FALSE:
                tmp = CONST_TRUE
            elif param_1 == CONST_FALSE and param_2 == CONST_FALSE:
                tmp = CONST_FALSE
        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de calcul XOR
    # ------------------------------------------------------------------------------------------------------------------
    def calc_xor(self, param_1, param_2):
        tmp = ""
        if (CONST_NOT in param_1 or param_1 in CONST_CHAR) and (CONST_NOT in param_2 or param_2 in CONST_CHAR):
            tmp = param_1 + '^' + param_2
        elif CONST_NOT in param_1 or param_1 in CONST_CHAR:
            tmp = param_1
        elif CONST_NOT in param_2 or param_2 in CONST_CHAR:
            tmp = param_2
        else:
            if param_1 == CONST_TRUE and param_2 == CONST_TRUE:
                tmp = CONST_FALSE
            elif param_1 == CONST_FALSE and param_2 == CONST_TRUE:
                tmp = CONST_TRUE
            elif param_1 == CONST_TRUE and param_2 == CONST_FALSE:
                tmp = CONST_TRUE
            elif param_1 == CONST_FALSE and param_2 == CONST_FALSE:
                tmp = CONST_FALSE
        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de remplacement de la valeur negative
    # ------------------------------------------------------------------------------------------------------------------
    def calc_neg(self, param_1):
        print(f'calc_neg_param_1 = {param_1}')
        if self.value[param_1] != '':
            # if self.value[param_1] == CONST_FALSE:
            if self.value[param_1] == CONST_TRUE:
                tmp = CONST_TRUE
                print(f'1 = {tmp}')
            else:
                tmp = CONST_FALSE
                print(f'2 = {tmp}')
        else:
            tmp = param_1
            print(f'3 = {tmp}')
            self.list_unknown.append(tmp)
        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de remplacement de la valeur positive
    # ------------------------------------------------------------------------------------------------------------------
    def calc_pos(self, param_1):
        if self.value[param_1] != '':
            tmp = self.value[param_1]
        else:
            tmp = param_1
            self.list_unknown.append(tmp)
        return tmp

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de recherche regex dans une string
    # ------------------------------------------------------------------------------------------------------------------
    def search_regex(self, string, regex):
        tuple_regex = list(set(re.findall(regex, string)))
        return tuple_regex

    # ------------------------------------------------------------------------------------------------------------------
    #   methode de recuperation des parametre
    # ------------------------------------------------------------------------------------------------------------------
    def recup_param(self, pair):
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
    #   methode de recuperation valeur
    # ------------------------------------------------------------------------------------------------------------------
    def recup_val(self, val):
        val = re.sub(r'''\(*\)*''', '', val)

        return val
