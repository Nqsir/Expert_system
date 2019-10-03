from Header.Header import *

from Modules.Get_list import translat_to_list
from Modules.Errors import display_errors_dict
from Modules.Solver import solver


def check_elements(x_file, logger_):
    rules = []
    facts = []
    queries = []
    fact = 0

    for x_line in x_file:
        facts_pattern = re.findall(r'''
                                   ^(=)([A-Z]+)|^([=])$       # =ABC or =
                                   ''', x_line, re.VERBOSE)
        queries_pattern = re.findall(r'''
                                     ^([?])([A-Z]+)$            # ?ABC
                                     ''', x_line, re.VERBOSE)
        rules_pattern = re.findall(r'''
                                   (^\(*!?[A-Z]\)*              # The starting expression (!A or (A or A
                                   ([\+\|\^]\(*!?[A-Z]\)*)*)    # The repeated scheme + or | or ^ and !A or A) or A
                                   (=>)                         # Equal
                                   (\(*!?[A-Z]\)*               # The starting expression (!A or (A or A
                                   ([\+\|\^]\(*!?[A-Z]\)*)*)$   # The repeated scheme + or | or ^ and !A or A) or A
                                    ''', x_line, re.VERBOSE)

        if queries_pattern:
            if not queries:
                for q in queries_pattern[0][1]:
                    queries.append(list(q))
            else:
                return 'query_1', x_line

        elif facts_pattern:
            if not facts:
                fact = 1
                for f in facts_pattern[0][1]:
                    facts.append(list(f))
            else:
                return 'fact_1', x_line

        elif rules_pattern:
            if '|' in rules_pattern[0][3] or '^' in rules_pattern[0][3]:
                return 'or', x_line
            if facts or queries:
                return 'rule_1', x_line
            if '(' in rules_pattern[0][0] or '(' in rules_pattern[0][3] \
                    or ')' in rules_pattern[0][0] or '(' in rules_pattern[0][3]:
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
            return 'term', x_line

    if not queries:
        return 'query_0', ''
    if not fact:
        return 'fact_0', ''
    if not rules:
        return 'rule_0', ''

    # -------------------------------- START Only prints ------------------------------------------
    max_l = len(max([_[0] for _ in rules], key=len))

    logger_.debug('\n=========== STARTING RULES =========== \n'
                  f'{"IF":{max_l + 5}s}\t{"THEN"}')
    logger_.debug(f'{"-" * max_l:{max_l + 5}s}\t{"------"}')
    for r in rules:
        logger_.debug(f'{r[0]:{max_l + 5}s}\t{r[1]:s}')
    logger_.debug('\n')

    logger_.debug(f'=========== FACTS ===========\n {facts}\n')

    logger_.debug(f'========== QUERIES ==========\n {queries}\n')
    # -------------------------------- END Only prints ------------------------------------------

    errors_ = translat_to_list(rules, logger_)
    if errors_:
        return errors_
    solver(rules, facts, queries)

    return OK


def extracting_file(file_):
    extract_file = []
    with open(file_, 'r') as in_file:
        for line in in_file:
            line = line.replace(' ', '')
            if not line.startswith('#') and line != '\n':
                if '#' in line:
                    rest = line.split('#')
                else:
                    rest = line.split('\n')

                extract_file.append(rest[0])

    return extract_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='py Expert_system.py')
    parser.add_argument('text_file', help='A text file containing instructions')
    parser.add_argument('-d', '--details', action='store_true', help='Detailed computation', default=False)
    args = parser.parse_args()
    logger = logging.getLogger()
    if args.details:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.debug('\n/*/-------\n Detailed mode activated \n/*/-------\n')
    args = parser.parse_args()

    file = os.path.join(os.getcwd(), args.text_file)

    if os.path.exists(file)and os.path.isfile(file) and file.endswith('.txt'):
        errors = []
        try:
            extracted_file = extracting_file(file)

            errors = check_elements(extracted_file, logger)
            if errors:
                display_errors_dict(errors)

        except PermissionError:
            sys.exit(print('\x1b[1;37;41m Permission error, failed opening the file \x1b[0m\n'))
    else:
        sys.exit(print(f'\x1b[1;37;41mThe selected file must be a text file i.e. with extension ".txt" \x1b[0m\n'))
