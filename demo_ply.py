import time
from ply.lex import lex

from mw import api

tokens = (
    'word',
    'number',
    'period',
    'qmark',
    'epoint',
    'comma',
    'colon',
    'scolon',
    'break',
    'whitespace',
    "etc"
)

t_word = r'[^\W\d]+'
t_number = r'[\d]+'
t_period = r'\.'
t_qmark = r'\?'
t_epoint = r'!'
t_comma = r','
t_colon = r':'
t_scolon = r';'
t_break = r'(\n|\n\r|\r\n)\s*(\n|\n\r|\r\n)+'
t_whitespace = r'[\n\r\s]+'
t_etc = r"."


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex()

session = api.Session("https://en.wikipedia.org/w/api.php")
common1 = session.revisions.get(638029546, properties={"content"})['*']

start = time.time()
for i in range(50):
    lexer.input(common1)
    while True:
        token = lexer.token()
        # print(token)
        if token is None:
            break

print("Tokenizing (text_split):", (time.time() - start)/50)
