import argparse
import os
import sys
import re


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='py Expert_system.py')
    parser.add_argument('text_file', help='A text file with instructions')
    args = parser.parse_args()

    file = os.path.join(os.getcwd(), args.text_file)

    if os.path.exists(file)and os.path.isfile(file) and file.endswith('.txt'):
        try:
            rules = []
            facts = []
            queries = []
            extracted_file = []
            with open(file, 'r') as in_file:
                for line in in_file:
                    if not line.startswith('#') and line != '\n':
                        if '#' in line:
                            rest = line.split('#')
                            extracted_file.append(rest[0])
                        else:
                            extracted_file.append(line)

            # DEBUG
            for ext in extracted_file:
                if ext.startswith('='):
                    queries.append(ext)
                elif ext.startswith('?'):
                    facts.append(ext)
                else:
                    rules.append(ext)

            if len(queries) > 1 or not queries:
                sys.exit(print('Problem with queries'))
            if len(facts) > 1 or not facts:
                sys.exit(print('Problem with facts'))
            if not rules:
                sys.exit(print('Problem with rules'))

            print(f'queries = {queries}')
            print(f'facts = {facts}')
            print(f'rules = {rules}')

        except PermissionError:
            print('Permission error, failed opening the file')
    else:
        print(f'The selected file must be a text file i.e. with extension ".txt"\n')
