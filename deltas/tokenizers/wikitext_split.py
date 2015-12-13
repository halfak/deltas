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
#re.compile(url, re.U).match("https://website.gov?param=value")

# Matches Chinese, Japanese and Korean characters.
cjk = (
    r'[' +
        r'\u4E00-\u62FF' +  # Unified Ideographs
            r'\u6300-\u77FF' +
            r'\u7800-\u8CFF' +
            r'\u8D00-\u9FCC' +
        r'\u3400-\u4DFF' +  # Unified Ideographs Ext A
        r'\U00020000-\U000215FF' + # Unified Ideographs Ext. B
            r'\U00021600-\U000230FF' +
            r'\U00023100-\U000245FF' +
            r'\U00024600-\U000260FF' +
            r'\U00026100-\U000275FF' +
            r'\U00027600-\U000290FF' +
            r'\U00029100-\U0002A6DF' +
        r'\uF900-\uFAFF' +  # Compatibility Ideographs
        r'\U0002F800-\U0002FA1F' +  # Compatibility Ideographs Suppl.
        r'\u3041-\u3096' +  # Hiragana
        r'\u30A0-\u30FF' +  # Katakana
        r'\u3400-\u4DB5' +  # Kanji
            r'\u4E00-\u9FCB' +
            r'\uF900-\uFA6A' +
        r'\u2E80-\u2FD5' +  # Kanji radicals
        r'\uFF5F-\uFF9F' +  # Katakana and Punctuation (Half Width)
        r'\x31F0-\x31FF' +  # Miscellaneous Japanese Symbols and Characters
            r'\x3220-\x3243' +
            r'\x3280-\x337F'
    r']'
)

LEXICON = [
    ('comment_start', r'<!--'),
    ('comment_end',   r'-->'),
    ("url",           url),
    ('entity',        r'&[a-z][a-z0-9]*;'),
    ('cjk',           cjk),
    ('tag',           r'<\\?([a-z][a-z0-9]*)\b[^>]*>'),
    ('number',        r'[\d]+'),
    ('word',          r'\w*[^\W\d]([\'’]*\w*)*'),
    ('period',        r'\.+'),
    ('qmark',         r'\?+'),
    ('epoint',        r'!+'),
    ('comma',         r',+'),
    ('colon',         r':+'),
    ('scolon',        r';+'),
    ('japan_punct',   r'[\x3000-\x303F]+'),
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
