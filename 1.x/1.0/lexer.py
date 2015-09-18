from UtopiaLexer import *

PAREN = 'PAREN'
SEP = 'SEP'
CONDITION = 'COND'
EQUALS = 'EQ'
NUM = 'NUM'
PROCEDURE = 'PROC'


def lexline(script):
    lex = lexer()

    lex.add_token_expr(r"^[\s]", None)
    lex.add_token_expr('^[()]', PAREN)
    lex.add_token_expr('^,', SEP)
    lex.add_token_expr(r"^(_|#)", CONDITION)
    lex.add_token_expr(r"^=", EQUALS)
    lex.add_token_expr(r"^[0-9]+(\.[0-9]+)?", NUM)
    lex.add_token_expr(r"^([\S])", PROCEDURE)

    return lex.lex(script)

def lexscript(script):
    script = script.split('\n')
    return [lexline(x) for x in script]


if __name__ == '__main__':
    print(lexscript(input()))
    input()
