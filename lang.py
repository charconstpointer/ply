import ply.lex as lex
from ply import yacc

f = open("inputs.foo", "r")
tokens = (
    'IDENT',
    'FUNC',
    'OP',
    'CP',
    'OB',
    'CB',
    'COMMA',
    'COMMENT',
    'EOL'
)

t_ignore = r'[ t\]'
t_OP = r'\('
t_COMMENT = r'\#'
t_OB = r'\{'
t_CP = r'\)'
t_EOL = r'\n'
t_CB = r'\}'
t_COMMA = r','


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_IDENT(t):
    r'[a-zA-Z0-9]+'
    if t.value == 'func':
        t.type = 'FUNC'
    return t


lexer = lex.lex()


class F:
    def __init__(self):
        self.args = []


funcs = {}
calls = {}

# lexer.input(f.read())
# while True:
#     tok = lexer.token()
#     if not tok:
#         break  # No more input
#     print(tok)

def p_program(p):
    'program : func funcs'
    print(p[1])


def p_funcs(p):
    'funcs : func func'


def p_func(p):
    'func : FUNC IDENT OP params CP OB body CB'
    f_name = p[2]
    fn = F()
    fn.args = p[4]
    funcs[f_name] = fn
    # print(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])


def p_func_no_params(p):
    'func : FUNC IDENT OP CP OB body CB'
    f_name = p[2]
    fn = F()
    fn.args = []
    funcs[f_name] = fn
    # print(p[1], p[2], p[3], p[4], p[5], p[6], p[7])


def p_params_single(p):
    'params : IDENT'
    p[0] = ('params', p[1])


def p_params_multi(p):
    'params : IDENT params'


def p_body_invoke(p):
    'body :  IDENT OP params CP '
    p[0] = ('invoke', p[1], p[3])
    f_name = p[1]
    fn = F()
    fn.args = p[3]
    calls[f_name] = fn

def p_body_empty(p):
    'body : '
    pass


def p_body_invoke_no_params(p):
    'body : IDENT OP CP'
    p[0] = ('invoke', p[1])


parser = yacc.yacc()
parser.parse(f.read())
for func in funcs:
    print("declared ", func, "with args", funcs[func].args)
for c in calls :
    print("calling ", c, "with args", calls[c].args)
# csv = csv_builder.csv()
# print(csv.columns)
#
# # while True:
# # try:
# #     # s = input('calc > ')   # Use raw_input on Python 2
# # except EOFError:
# #     break
