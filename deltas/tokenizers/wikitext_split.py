import re

from .tokenizer import RegexTokenizer

LEXICON = [
    ('comment_start', r'<!--'),
    ('comment_end',   r'-->'),
    ('entity',        r'&[a-z][a-z0-9]*;'),
    ('word',          r'[^[\W\d]+'),
    ('number',        r'[\d]+'),
    ('tag',           r'<\\?([a-z][a-z0-9]*)\b[^>]*>'),
    ('period',        r'\.+'),
    ('qmark',         r'\?+'),
    ('epoint',        r'!+'),
    ('comma',         r',+'),
    ('colon',         r':+'),
    ('scolon',        r';+'),
    ('break',         r'(\n|\n\r|\r\n)\s*(\n|\n\r|\r\n)+'),
    ('whitespace',    r'[\n\r\s]+'),
    ('dbrack_open',   r'\[\['),
    ('dbrack_close',  r'\]\]'),
    ('brack_open',    r'\['),
    ('brack_close',   r'\]'),
    ('tab_open',      r'\{\|'),
    ('tab_close',     r'\|\}'),
    ('dcurly_open',   r'\{\{'),
    ('dcurly_close',  r'\}\}'),
    ('curly_open',    r'\{'),
    ('curly_close',   r'\}'),
    ("bold",          r"'''"),
    ("italic",        r"''"),
    ("equals",        r"=+"),
    ("etc",           r".")
]

wikitext_split = RegexTokenizer(LEXICON)
