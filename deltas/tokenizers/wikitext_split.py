import re

from .tokenizer import RegexTokenizer

PLAIN_PROTO = [r'bitcoin', r'geo', r'magnet', r'mailto', r'news', r'sips?',
               r'tel', r'urn']
SLASHED_PROTO = [r'', r'ftp', r'ftps', r'git', r'gopher', r'https?', r'ircs?',
                 r'mms', r'nntp', r'redis', r'sftp', r'ssh', r'svn', r'telnet',
                 r'worldwind', r'xmpp']
ADDRESS = (
    r'(?:\S+(?::\S*)?@)?' +
    r'(?:' +
        r'(?!10(?:\.\d{1,3}){3})' +
        r'(?!127(?:\.\d{1,3}){3})' +
        r'(?!169\.254(?:\.\d{1,3}){2})' +
        r'(?!192\.168(?:\.\d{1,3}){2})' +
        r'(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})' +
        r'(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])' +
        r'(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}' +
        r'(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|' +
        r'(?:' +
            r'(?:[a-z\u00a1-\uffff0-9]+-?)*' +
            r'[a-z\u00a1-\uffff0-9]+' +
        r')' +
        r'(?:' +
            r'\.(?:[a-z\u00a1-\uffff0-9]+-?)*' +
            r'[a-z\u00a1-\uffff0-9]+' +
        r')*' +
        r'(?:\.(?:[a-z\u00a1-\uffff]{2,}))?' +
    r')' +
    r'(?::\d{2,5})?' +
    r'(?:[^a-z\u00a1-\uffff0-9][^\s]*)?'
)
url = (
    r'(' + \
        r'(' + '|'.join(PLAIN_PROTO) + r')\:|' + \
        r'(' + '|'.join(SLASHED_PROTO) + r')\:\/\/' + \
    r')' + ADDRESS
)
re.compile(url, re.U).match("https://website.gov?param=value")


LEXICON = [
    ('comment_start', r'<!--'),
    ('comment_end',   r'-->'),
    ("url",           url),
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
