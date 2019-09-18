
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
        'loop': f'Error\n\n'
              f'A loop has been found concerning : \x1b[1;37;41m {err[1]} \x1b[0m\n\n',
    }

    print(f'\n{dictionary[err[0]]}')
