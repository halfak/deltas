
from .tokenizer import TokenizerPipeline
from .tokenizer import CJKSegmenter
from .wikitext_split import wikitext_split

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

CJK_LEXICON = {
    'cjk': cjk_char,
    'japanese': jap_char,
    'korean': kor_char,
}

wikitext_split_w_cjk = TokenizerPipeline(wikitext_split, CJKSegmenter(CJK_LEXICON)) # noqa
