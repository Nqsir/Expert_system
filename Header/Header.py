import re
import argparse
import os
import sys
import re
import logging

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
