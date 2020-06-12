from .tokenizer import RegexTokenizer

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
# re.compile(url, re.U).match("https://website.gov?param=value")

devangari_word = r'\u0901-\u0963'
arabic_word = r'\u0601-\u061A' + \
              r'\u061C-\u0669' + \
              r'\u06D5-\u06EF'
bengali_word = r'\u0980-\u09FF'
korean_word = r'\uac00-\ud7a3'

combined_word = devangari_word + arabic_word + bengali_word + korean_word

cjk_re = r'\u3040-\u30ff' + r'\u4e00-\u9FFF'

cjk = r'[' + cjk_re + ']'

word = r'(?:[^\W\d' + cjk_re + r']|[' + combined_word + r'])' + \
       r'[\w' + combined_word + r']*' + \
       r'(?:[\'’](?:[\w' + combined_word + r']+|(?=(?:$|\s))))*'

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

LEXICON_LATIN = LEXICON.copy()
LEXICON_LATIN.insert(-2, ('cjk', cjk))
wikitext_split = RegexTokenizer(LEXICON_LATIN)

LEXICON_CJK = LEXICON.copy()
LEXICON_CJK.insert(0, ('cjk', cjk))
wikitext_split_cjk = RegexTokenizer(LEXICON_CJK)
