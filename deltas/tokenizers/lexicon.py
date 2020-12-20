#       REGEXP CHEATSHEET
#
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
# \b    used to find a match at the beginning or end of a word.

# Unified Ideographs, Unified Ideographs Ext A,
# Unified Ideographs Ext. B, Compatibility Ideographs,
# Compatibility Ideographs Suppl.
chinese_n_misc_char = r'\u4E00-\u62FF' + \
                      r'\u3400-\u4DFF' + \
                      r'\U00020000-\U000215FF' + \
                      r'\uF900-\uFAFF' + \
                      r'\U0002F800-\U0002FA1F' + \
                      r'\u6300-\u77FF' + \
                      r'\u7800-\u8CFF' + \
                      r'\u8D00-\u9FCC' + \
                      r'\U00021600-\U000230FF' + \
                      r'\U00023100-\U000245FF' + \
                      r'\U00024600-\U000260FF' + \
                      r'\U00026100-\U000275FF' + \
                      r'\U00027600-\U000290FF' + \
                      r'\U00029100-\U0002A6DF' + \
                      r'\u4E00-\u9FCB' + \
                      r'\uF900-\uFA6A' + \
                      r'\u3220-\u3243' + \
                      r'\u3280-\u337F'

# Hiragana, Katakana, Kanji, Kanji radicals,
# Katakana and Punctuation (Half Width), Misc Symbols and Chars
jap_char = r'\u3041-\u3096' + \
           r'\u30A0-\u30FF' + \
           r'\u3400-\u4DB5' + \
           r'\u2E80-\u2FD5' + \
           r'\uFF5F-\uFF9F' + \
           r'\u31F0-\u31FF'

# hangul syllables, hangul jamo, hangul, hangul, hangul
kor_char = r'\uAC00-\uD7AF' + \
           r'\u1100-\u11FF' + \
           r'\u3130–\u318F' + \
           r'\uA960–\uA97F' + \
           r'\uD7B0–\uD7FF'

cjk_char = chinese_n_misc_char + jap_char + kor_char

cjk_word = r'(?=[' + cjk_char + r'])' + \
       r'[' + cjk_char + r']*' + \
       r'(?:[\'’](?:[' + cjk_char + r']+|(?=(?:$|\s))))*'

devangari_char = r'\u0901-\u0963'

arabic_char = r'\u0601-\u061A' + \
              r'\u061C-\u0669' + \
              r'\u06D5-\u06EF'

bengali_char = r'\u0980-\u09FF'

combined_char = devangari_char + \
                arabic_char + \
                bengali_char


# (anything that is not(non-alphanmeric, decimal digit) or is combined_char) +
# any number of combined_char repetitions +
# any number of combined_char repetitions encapsulated in apostrophes

word = r'(?:[^\W\d]|[' + combined_char + r'])' + \
       r'[\w' + combined_char + r']*' + \
       r'(?:[\'’](?:[\w' + combined_char + r']+|(?=(?:$|\s))))*'

plain_proto = [r'bitcoin', r'geo', r'magnet', r'mailto', r'news', r'sips?',
               r'tel', r'urn']

slashed_proto = [r'https?', r'ftp', r'ftps', r'git', r'gopher', r'ircs?',
                 r'mms', r'nntp', r'redis', r'sftp', r'ssh', r'svn', r'telnet',
                 r'worldwind', r'xmpp']

address = r'[^\s/$.?#][^|<>\s{}]*'

url = (
    r'(?:' +  # noqa
        r'(?:' + '|'.join(plain_proto) + r')\:|' +  # noqa
        r'(?:(?:' + '|'.join(slashed_proto) + r')\:)?\/\/' +
    r')' + address
)

number = r'[0-9][0-9\.\,]*(e[0-9]+)*|[\.\,][0-9][0-9\.\,]*(e[0-9]+)*'

TEXT_SPLIT_LEXICON = [
    ('word', r'[^\W\d]+'),
    ('number', number),
    ('period', r'\.'),
    ('qmark', r'\?'),
    ('epoint', r'!'),
    ('comma', r','),
    ('colon', r':'),
    ('scolon', r';'),
    ('break', r'(\n|\n\r|\r\n)\s*(\n|\n\r|\r\n)+'),
    ('whitespace', r'[\n\r\s]+'),
    ("etc", r".")
]

CJK_LEXICON = {
    'cjk': r'[' + cjk_char + r']',
    'chinese': r'[' + chinese_n_misc_char + r']',
    'japanese': r'[' + jap_char + r']',
    'korean': r'[' + kor_char + r']',
}

WIKITEXT_SPLIT_LEXICON = [
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
    ('number', number),
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
