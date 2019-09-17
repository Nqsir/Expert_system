import argparse
import os
import re


OK = 0


def disp_errors_dict(err):
    dictionary = {
        'query_0': f'Expression probably false\n\n'
                   f'Unexpected query, \x1b[1;37;41m no query found \x1b[0m\n\n',
        'query_1': f'Expression probably false\n\n'
                   f'Unexpected query, multiple queries : \x1b[1;37;41m {err[1]} \x1b[0m\n\n',
        'fact_0': f'Expression probably false\n\n'
                  f'Unexpected fact, \x1b[1;37;41m no fact found \x1b[0m\n\n',
        'fact_1': f'Expression probably false\n\n'
                  f'Unexpected fact, multiple facts : \x1b[1;37;41m {err[1]} \x1b[0m\n\n',
        'rule': f'Expression probably false\n\n'
                f'Unexpected rule : \x1b[1;37;41m {err[1]} \x1b[0m\n\n',
        'rule_0': f'Expression probably false\n\n'
                  f'Unexpected rule, \x1b[1;37;41m no rule found \x1b[0m\n\n',
        'rule_1': f'Expression probably false\n\n'
                  f'Unexpected rule order : \x1b[1;37;41m {err[1]} \x1b[0m\n\n',
        'par1': f'Expression probably false\n\n'
                f'Unexpected rule, parentheses in if expression : \x1b[1;37;41m {err[1]} \x1b[0m\n\n',
        'par2': f'Expression probably false\n\n'
                f'Unexpected rule, parentheses in then expression : \x1b[1;37;41m {err[1]} \x1b[0m\n\n',
        'or': f'Expression probably false\n\n'
              f'Unexpected rule, ambiguous condition in then expression : \x1b[1;37;41m {err[1]} \x1b[0m\n\n',
    }

    print(f'\n{dictionary[err[0]]}')


def check_elements(x_file):
    rules = []
    facts = []
    fact = 0
    queries = []

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

            exp_if = re.findall(r'''([A-Z])''', rules_pattern[0][0])
            exp_then = re.findall(r'''([A-Z])''', rules_pattern[0][3])

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

    print('\nrules = \n'
          f'{"IF":45s}\t{"THEN"}')
    for r in rules:
        print(f'{r[0]:45s}\t{r[1]:s}')
    print('\n')
    print(f'facts = {facts}')
    print(f'queries = {queries}')

    return OK


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='py Expert_system.py')
    parser.add_argument('text_file', help='A text file with instructions')
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
