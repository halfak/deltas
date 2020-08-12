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

cjk = chinese_n_misc_char + jap_char + kor_char

devangari_word = r'\u0901-\u0963'

arabic_word = r'\u0601-\u061A' + \
              r'\u061C-\u0669' + \
              r'\u06D5-\u06EF'

bengali_word = r'\u0980-\u09FF'
