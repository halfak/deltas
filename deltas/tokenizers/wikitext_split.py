from .tokenizer import RegexTokenizer
from . import lexicon_chars

PLAIN_PROTO = [r'bitcoin', r'geo', r'magnet', r'mailto', r'news', r'sips?',
               r'tel', r'urn']
SLASHED_PROTO = [r'https?', r'ftp', r'ftps', r'git', r'gopher', r'ircs?',
                 r'mms', r'nntp', r'redis', r'sftp', r'ssh', r'svn', r'telnet',
                 r'worldwind', r'xmpp']
ADDRESS = r'[^\s/$.?#][^|<>\s{}]*'

url = (
    r'(?:' +  # noqa
        r'(?:' + '|'.join(PLAIN_PROTO) + r')\:|' +  # noqa
        r'(?:(?:' + '|'.join(SLASHED_PROTO) + r')\:)?\/\/' +
    r')' + ADDRESS
)

combined_word = lexicon_chars.devangari_word + \
                lexicon_chars.arabic_word + \
                lexicon_chars.bengali_word

# ?     ab? will match either ‘a’ or ‘ab’
# []	Used to indicate a set of characters. In a set
# ^	    If the first character of the set is '^', all the
#       characters that are not in the set will be matched. For example,
#       [^5] will match any character except '5'
# \w	matches any alphanumeric character and the underscore; this is
#       equivalent to the set [a-zA-Z0-9_]
# \W	matches any non-alphanumeric character; this is equivalent to
#       the set [^a-zA-Z0-9_]
# \d	matches any decimal digit; this is equivalent to the set [0-9]
# |	    or
# \s	matches any whitespace character, this is equivalent to the
#       set [ \t\n\r\f\v]
# $	    Matches the end of the string or just before the newline at the
#       end of the string
# *     match 0 or more repetitions of the preceding RE, as many repetitions as
#       are possible. ab* will match ‘a’, ‘ab’, or ‘a’ followed by any number
#       of ‘b’s.

# (anything that is not(non-alphanmeric, decimal digit) or word_char) +
# any number of word_char repetitions +
# any number of word_char repetitions encapsulated in apostrophes

word = r'(?:[^\W\d]|[' + combined_word + r'])' + \
       r'[\w' + combined_word + r']*' + \
       r'(?:[\'’](?:[\w' + combined_word + r']+|(?=(?:$|\s))))*'

cjk_word = r'(?=[' + lexicon_chars.cjk + r'])' + \
       r'[' + lexicon_chars.cjk + r']*' + \
       r'(?:[\'’](?:[' + lexicon_chars.cjk + r']+|(?=(?:$|\s))))*'

LEXICON = [
    ('break', r'(?:\n\r?|\r\n)\s*(?:\n\r?|\r\n)+'),
    ('whitespace', r'(?:\n\r?|[^\S\n\r]+)'),
    ("url", url),
    ("equals", r"=+"),
    ("bar", r"\|"),
    ('entity', r'&[a-z][a-z0-9]*;'),
    ('ref_open', r'<ref\b(?:\/(?!>)|[^>\/])*>'),
    ('ref_close', r'</ref\b[^>]*>'),
    ('ref_singleton', r'<ref\b(?:\/(?!>)|[^/>])*\/>'),
    ('tag', r'</?([a-z][a-z0-9]*)\b[^>]*>'),
    ('number', r'\d+'),
    ("bold", r"'''"),
    ("italic", r"''"),
    ('japan_punct', r'[\u3000-\u303F]'),
    ('cjk_word', cjk_word),
    ('word', word),
    ('tab_open', r'\{\|'),
    ('tab_close', r'\|\}'),
    ('dbrack_open', r'\[\['),
    ('dbrack_close', r'\]\]'),
    ('brack_open', r'\['),
    ('brack_close', r'\]'),
    ('paren_open', r'\('),
    ('paren_close', r'\)'),
    ('dcurly_open', r'\{\{'),
    ('dcurly_close', r'\}\}'),
    ('curly_open', r'\{'),
    ('curly_close', r'\}'),
    ('period', r'\.+'),
    ('qmark', r'\?+'),
    ('epoint', r'!+'),
    ('comma', r',+'),
    ('colon', r':+'),
    ('scolon', r';+'),
    ('comment_start', r'<!--'),
    ('comment_end', r'-->'),
    ('danda', r'।|॥'),
    ("etc", r"."),
]

wikitext_split = RegexTokenizer(LEXICON)
