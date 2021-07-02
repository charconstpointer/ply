import ply.lex as lex
from ply import yacc
import os
import time

tokens = (
    'IDENT',
    'END',
    'RUN',
    'OP',
    'CP'
)


def t_IDENT(t):
    r'[a-z]+'
    if t.value == "run":
        t.type = 'RUN'
    return t


def t_END(t):
    r';'
    print("END")

    # Define a rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_OP = r'{'
t_CP = r'}'
t_RUN = r'[a-z]+'
t_ignore = r'[ ]+'
lexer = lex.lex()
# inp = "run {foo bar baz clazz}"
# lexer.input(inp)


#
# # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok:
#         break  # No more input
#     print(tok)
cmds = []
results = {}

def execute(target, *args):
    for arg in args:
        print(arg)
    start_time = time.time()
    import subprocess
    output = subprocess.check_output(target, shell=True)
    results[target] = output
    # print("--- %s seconds ---" % (time.time() - start_time))


def p_program_e(p):
    """program : RUN OP exprs CP"""
    print(p[1], p[2], p[3], p[4])

def p_exprs(p):
    'exprs : expr expr'

def p_expr_single(p):
    'expr : IDENT'
    print("run -> ", p[1])
    cmds.append(p[1])


def p_expr_multi(p):
    'expr : IDENT OP args CP'
    cmds.append(p[1])

def p_expr_many(p):
    'expr : IDENT expr'
    cmds.append(p[1])


def p_args_single(p):
    'args : IDENT'
    # cmds.append(p[1])
    p[0] = p[1]

def p_args_multi(p):
    'args : IDENT args'
    # cmds.append(p[1])
    if p[2] is None:
        p[0] = p[1]
    else:
        p[0] = p[1], p[2]
    print(p[0])


f = open("inputs.foo", "r")
parser = yacc.yacc()
parser.parse(f.read())
print(cmds)

# while True:
# try:
#     # s = input('calc > ')   # Use raw_input on Python 2
# except EOFError:
#     break
