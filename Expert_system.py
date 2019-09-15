import argparse
import os
import sys
import re


def check_elements(x_file):
    elements = []
    rules = []
    facts = []
    queries = []

    # Link to the atual REGEX working, still need a lot of parse : https://regex101.com/r/2x2D3C/4

    for x_line in x_file:
        x_line = x_line.replace(' ', '')
        print(f'{x_line}')
        facts_pattern = re.findall(r'''
                                   ^([=])([A-Z]*)
                                   '''
                                   , x_line, re.VERBOSE)
        queries_pattern = re.findall(r'''
                                     ^([?])([A-Z]*) 
                                     '''
                                     , x_line, re.VERBOSE)
        rules_pattern = re.findall(r'''
                                   ^(\(*!?[A-Z])
                                   (([\+\|\^]\(*!?[A-Z]\)*)*)
                                   (<=>|=>)
                                   (\(*!?[A-Z])
                                   (([\+\|\^]\(*!?[A-Z]\)*)*)
                                    ''', x_line, re.VERBOSE)
        # print(rules_pattern)
        # print(queries_pattern)
        # print(facts_pattern)
        # if rules_pattern:
        #     print(f'Rules pattern:')
        #     for elem in rules_pattern:
        #         print(f'elem = {elem}')

    print(f'elements = {elements}')

    # Renvoyer equivalent list gauche list droite (conditions / conclusion)
    # Sur liste gquche rajouter pre;ier element / char '(' et dernier element ')'

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='py Expert_system.py')
    parser.add_argument('text_file', help='A text file with instructions')
    args = parser.parse_args()

    file = os.path.join(os.getcwd(), args.text_file)

    if os.path.exists(file)and os.path.isfile(file) and file.endswith('.txt'):
        try:
            extracted_file = []
            with open(file, 'r') as in_file:
                for line in in_file:
                    if not line.startswith('#') and line != '\n':
                        if '#' in line:
                            rest = line.split('#')
                            extracted_file.append(rest[0])
                        else:
                            rest = line.split('\n')
                            extracted_file.append(rest[0])

            check_elements(extracted_file)

            # if len(queries) > 1 or not queries:
            #     sys.exit(print('Problem with queries'))
            # if len(facts) > 1 or not facts:
            #     sys.exit(print('Problem with facts'))
            # if not rules:
            #     sys.exit(print('Problem with rules'))

        except PermissionError:
            print('Permission error, failed opening the file')
    else:
        print(f'The selected file must be a text file i.e. with extension ".txt"\n')
