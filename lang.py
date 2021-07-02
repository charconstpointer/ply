from functools import reduce

import ply.lex as lex
from ply import yacc
import time

tokens = (
    'VAL',
    'COMMA'
)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_VAL = r'[a-zA-Z0-9"]+'
t_COMMA = r','
lexer = lex.lex()
f = open("inputs.foo", "r")


# lexer.input(f.read())

# #
# # # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok:
#         break  # No more input
#     print(tok)
# cmds = []
# results = {}
#
#
# def execute(target, *args):
#     for arg in args:
#         print(arg)
#     start_time = time.time()
#     import subprocess
#     output = subprocess.check_output(target, shell=True)
#     results[target] = output
#     # print("--- %s seconds ---" % (time.time() - start_time))
#
#
# def p_program_e(p):
#     """program : RUN OP exprs CP"""
#     print(p[1], p[2], p[3], p[4])
#
#
# def p_exprs(p):
#     'exprs : expr expr'
#
#
# def p_expr_single(p):
#     'expr : IDENT'
#     print("run -> ", p[1])
#     cmds.append(p[1])
#
#
# def p_expr_multi(p):
#     'expr : IDENT OP args CP'
#     cmds.append(p[1])
#
#
# def p_expr_many(p):
#     'expr : IDENT expr'
#     cmds.append(p[1])
#
#
# def p_args_single(p):
#     'args : IDENT'
#     # cmds.append(p[1])
#     p[0] = p[1]
#
#
# def p_args_multi(p):
#     'args : IDENT args'
#     # cmds.append(p[1])
#     if p[2] is None:
#         p[0] = p[1]
#     else:
#         p[0] = p[1], p[2]
#     print(p[0])
#
#
class Csv:
    def __init__(self, columns):
        self.columns = columns


class CsvBuilder:
    def __init__(self):
        self.columns = {}
        self.order = {}

    def insert_cols(self, cols):
        columns = str.split(cols, " ")
        for i, c in enumerate(columns):
            print(i, c)
            self.columns[c] = []
            self.order[i] = c

    def insert_rows(self, param):
        for row in param:
            values = str.split(row, " ")
            for i, value in enumerate(values):
                col = self.order[i]
                self.columns[col].append(value)
        print(self.columns)

    def csv(self):
        return Csv(self.columns)


# csv_builder = CsvBuilder()


def p_file(p):
    'file : header rows'
    print(p[1], p[2])
    # csv_builder.insert_cols(p[1])
    # csv_builder.insert_rows(p[2])


def p_header(p):
    'header : row'
    p[0] = p[1]


def p_rows(p):
    'rows : row row'
    p[0] = p[1], p[2]


def p_row_single_field(p):
    'row : VAL'
    p[0] = p[1]


def p_row(p):
    'row : VAL COMMA row'
    p[0] = ('row', p[1], p[3])


parser = yacc.yacc()
parser.parse(f.read())
# csv = csv_builder.csv()
# print(csv.columns)
#
# # while True:
# # try:
# #     # s = input('calc > ')   # Use raw_input on Python 2
# # except EOFError:
# #     break
