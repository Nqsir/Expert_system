import re
import argparse
import os
import sys
import re

from Errors import disp_errors_dict

from get_list import translat_to_list
from get_list import to_list

from resolver import resolver

from File_calc_value import calc_neg
from File_calc_value import calc_pos

from File_unitary import operation_unitary
from File_and import operation_and
from File_or import operation_or
from File_xor import operation_xor

from File_useful_function import search_regex
from File_useful_function import recup_param
from File_useful_function import recup_val

OK = 0

CONST_CHAR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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