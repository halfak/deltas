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

# Matches Chinese, Japanese and Korean characters.
cjk_char = (
    r'[' +
    r'\uAC00-\uD7AF' +  # hangul syllables
    r'\u1100-\u11FF' +  # hangul jamo
    r'\u3130–\u318F' +  # hangul
    r'\uA960–\uA97F' +  # hangul
    r'\uD7B0–\uD7FF' +  # hangul
    r'\u4E00-\u62FF' +  # noqa Unified Ideographs
    r'\u6300-\u77FF' +
    r'\u7800-\u8CFF' +
    r'\u8D00-\u9FCC' +
    r'\u3400-\u4DFF' +  # Unified Ideographs Ext A
    r'\U00020000-\U000215FF' +  # Unified Ideographs Ext. B
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
    r'\u31F0-\u31FF' +  # Miscellaneous Japanese Symbols and Characters
    r'\u3220-\u3243' +
    r'\u3280-\u337F' +
    r']'
)

jap_char = (
    r'[' +
    r'\u3041-\u3096' +  # Hiragana
    r'\u30A0-\u30FF' +  # Katakana
    r'\u3400-\u4DB5' +  # Kanji
    r'\u2E80-\u2FD5' +  # Kanji radicals
    r'\uFF5F-\uFF9F' +  # Katakana and Punctuation (Half Width)
    r'\u31F0-\u31FF' +  # Miscellaneous Japanese Symbols and Characters
    r']'
)

kor_char = (
    r'[' +
    r'\uAC00-\uD7AF' +  # hangul syllables
    r'\u1100-\u11FF' +  # hangul jamo
    r'\u3130–\u318F' +  # hangul
    r'\uA960–\uA97F' +  # hangul
    r'\uD7B0–\uD7FF' +  # hangul
    r']'
)

cjk = r'\uAC00-\uD7AF' + \
        r'\u1100-\u11FF' + \
        r'\u3130–\u318F' + \
        r'\uA960–\uA97F' + \
        r'\uD7B0–\uD7FF' + \
        r'\u4E00-\u62FF' + \
        r'\u6300-\u77FF' + \
        r'\u7800-\u8CFF' + \
        r'\u8D00-\u9FCC' + \
        r'\u3400-\u4DFF' + \
        r'\U00020000-\U000215FF' + \
        r'\U00021600-\U000230FF' + \
        r'\U00023100-\U000245FF' + \
        r'\U00024600-\U000260FF' + \
        r'\U00026100-\U000275FF' + \
        r'\U00027600-\U000290FF' + \
        r'\U00029100-\U0002A6DF' + \
        r'\uF900-\uFAFF' + \
        r'\U0002F800-\U0002FA1F' + \
        r'\u3041-\u3096' + \
        r'\u30A0-\u30FF' + \
        r'\u3400-\u4DB5' + \
        r'\u4E00-\u9FCB' + \
        r'\uF900-\uFA6A' + \
        r'\u2E80-\u2FD5' + \
        r'\uFF5F-\uFF9F' + \
        r'\u31F0-\u31FF' + \
        r'\u3220-\u3243' + \
        r'\u3280-\u337F'

devangari_word = r'\u0901-\u0963'
arabic_word = r'\u0601-\u061A' + \
              r'\u061C-\u0669' + \
              r'\u06D5-\u06EF'
bengali_word = r'\u0980-\u09FF'
combined_word = devangari_word + arabic_word + bengali_word

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

cjk_word = r'(?=[' + cjk + r'])' + \
       r'[' + cjk + r']*' + \
       r'(?:[\'’](?:[' + cjk + r']+|(?=(?:$|\s))))*'

CJK_LEXICON = {
    'cjk': cjk_char,
    'japanese': jap_char,
    'korean': kor_char,
}

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

wikitext_split = RegexTokenizer(LEXICON, CJK_LEXICON)
