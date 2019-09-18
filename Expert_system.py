import argparse
import os
import re
from Errors import disp_errors_dict
from get_list import *

OK = 0


def check_elements(x_file):
    rules = []
    facts = []
    queries = []
    fact = 0

    # Link to the working REGEX, still need a lot of parse : https://regex101.com/r/2x2D3C/6

    for x_line in x_file:
        facts_pattern = re.findall(r'''
                                   ^([=])([A-Z]+)|^([=])$       # =ABC or =
                                   '''
                                   , x_line, re.VERBOSE)
        queries_pattern = re.findall(r'''
                                     ^([?])([A-Z]+)$            # ?ABC
                                     '''
                                     , x_line, re.VERBOSE)
        rules_pattern = re.findall(r'''
                                   (^\(*!?[A-Z]\)*              # The starting expression (!A or (A or A
                                   ([\+\|\^]\(*!?[A-Z]\)*)*)    # The repeated scheme + or | or ^ and !A or A) or A
                                   (=>)                         # Equal
                                   (\(*!?[A-Z]\)*               # The starting expression (!A or (A or A
                                   ([\+\|\^]\(*!?[A-Z]\)*)*)$   # The repeated scheme + or | or ^ and !A or A) or A
                                    ''', x_line, re.VERBOSE)

        if queries_pattern:
            if not queries:
                queries.append(queries_pattern[0][1])
            else:
                return 'query_1', x_line

        elif facts_pattern:
            if not facts:
                facts.append(facts_pattern[0][1])
                fact = 1
            else:
                return 'fact_1', x_line

        elif rules_pattern:
            if '|' in rules_pattern[0][3]:
                return 'or', x_line
            if facts or queries:
                return 'rule_1', x_line
            if ('(' or ')') in rules_pattern[0][0] or rules_pattern[0][3]:
                open_1 = len([_ for _ in (rules_pattern[0][0]) if _ == '('])
                close_1 = len([_ for _ in (rules_pattern[0][0]) if _ == ')'])
                open_2 = len([_ for _ in (rules_pattern[0][3]) if _ == '('])
                close_2 = len([_ for _ in (rules_pattern[0][3]) if _ == ')'])
                if open_1 != close_1:
                    return 'par1', x_line
                if open_2 != close_2:
                    return 'par2', x_line

            exp_if = re.findall(r'''(!?[A-Z])''', rules_pattern[0][0])
            exp_then = re.findall(r'''(!?[A-Z])''', rules_pattern[0][3])

            for l in exp_if:
                if l in exp_then:
                    return 'or', x_line

            rules.append([f'({rules_pattern[0][0]})', re.sub(r'''\(*\)*''', '', rules_pattern[0][3])])
        else:
            return 'rule', x_line

    if not queries:
        return 'query_0', ''
    if not fact:
        return 'fact_0', ''
    if not rules:
        return 'rule_0', ''

    max_l = len(max([_[0] for _ in rules], key=len))

    print('\nrules = \n'
          f'{"IF":{max_l + 5}s}\t{"THEN"}')
    print(f'{"-------":{max_l + 5}s}\t{"-------"}')
    for r in rules:
        print(f'{r[0]:{max_l + 5}s}\t{r[1]:s}')
    print('\n')

    print(f'facts = {facts}')
    print(f'queries = {queries}')

    errors = translat_to_list(rules)
    if errors:
        return errors

    return OK


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='py Expert_system.py')
    parser.add_argument('text_file', help='A text file containing instructions')
    args = parser.parse_args()

    file = os.path.join(os.getcwd(), args.text_file)

    if os.path.exists(file)and os.path.isfile(file) and file.endswith('.txt'):
        errors = []
        try:
            extracted_file = []
            with open(file, 'r') as in_file:
                for line in in_file:
                    line = line.replace(' ', '')
                    if not line.startswith('#') and line != '\n':
                        if '#' in line:
                            rest = line.split('#')
                        else:
                            rest = line.split('\n')

                        extracted_file.append(rest[0])

            errors = check_elements(extracted_file)
            if errors:
                disp_errors_dict(errors)

        except PermissionError:
            print('\x1b[1;37;41m Permission error, failed opening the file \x1b[0m\n')
    else:
        print(f'\x1b[1;37;41mThe selected file must be a text file i.e. with extension ".txt" \x1b[0m\n')
