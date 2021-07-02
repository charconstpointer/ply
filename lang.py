import ply.lex as lex
from ply import yacc
import collections


def flatten(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


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

t_ignore = ' \t'
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


def t_error(t):
    t.lexer.skip(1)


lexer = lex.lex()


class F:
    def __init__(self, name, args):
        self.args = args
        self.name = name


funcs = {}
calls = []
params = []


def p_program(p):
    'program : funcs'


def p_funcs(p):
    'funcs : func funcs'


def p_funcs_empty(p):
    'funcs : '


def p_func(p):
    'func : FUNC IDENT OP params CP OB bodies CB'
    # print("declaring func: ", p[2])
    # print("\twith args: ", flatten(p[4]))
    f_name = p[2]
    args = []
    if p[4] is not None:
        args = flatten(p[4])
    fn = F(f_name, args)
    funcs[f_name] = fn


def p_bodies(p):
    'bodies : body'


def p_params(p):
    'params : IDENT params'
    p[0] = p[1]
    params.append(p[1])


def p_params_many(p):
    'params : IDENT COMMA params'
    p[0] = p[1], p[3]


def p_params_empty(p):
    'params : '


def p_body_(p):
    'body : IDENT OP CP bodies'
    fn = p[1]
    calls.append([fn, []])


def p_body_params(p):
    'body : IDENT OP params CP bodies'
    fn = p[1]
    args = flatten(p[3])
    calls.append([fn, args])


def p_body_empty(p):
    'body : '


def p_error(p):
    # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    print('Syntax error in input! Parser State:{} {} . {}'
          .format(parser.state,
                  stack_state_str,
                  p))


parser = yacc.yacc()
parser.parse(f.read())
print(' '.join("*" * 25))
for call in calls:
    f_name = call[0]
    with_args = call[1]
    if f_name not in funcs:
        print("function", f_name, "is not declared")
        continue
    fn = funcs[f_name]
    if len(fn.args) != len(with_args):
        word = "was" if len(fn.args) < 2 else "were"
        print("function", f_name, "expects", len(fn.args), "arguments, instead", len(with_args), word, "provided")
