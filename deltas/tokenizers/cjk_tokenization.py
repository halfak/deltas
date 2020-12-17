import re
import jieba as ch_jieba
from sudachipy import tokenizer as jp_tokenizer
from sudachipy import dictionary as jp_dictionary
from konlpy.tag import Okt as ko_okt


CH_JIEBA = ch_jieba.Tokenizer()
JAP_SUDACHY = None
KOR_KONLPY_OKT = None


def get_ch_tokenizer():
    if CH_JIEBA.initialized is False:
        CH_JIEBA.initialize()
    return CH_JIEBA


def get_jap_tokenizer():
    global JAP_SUDACHY
    if JAP_SUDACHY is None:
        JAP_SUDACHY = jp_dictionary.Dictionary().create()
    return JAP_SUDACHY


def get_kor_tokenizer():
    global KOR_KONLPY_OKT
    if KOR_KONLPY_OKT is None:
        KOR_KONLPY_OKT = ko_okt()
    return KOR_KONLPY_OKT


def lng_decision(text, cjk_lexicon, lng_frac_par=0.25):
    regex_cjk = re.compile(cjk_lexicon['cjk'])
    regex_japanese = re.compile(cjk_lexicon['japanese'])
    regex_korean = re.compile(cjk_lexicon['korean'])
        
    cjk_symbols = len(regex_cjk.findall(text))
    jap_symbols = len(regex_japanese.findall(text))
    kor_symbols = len(regex_korean.findall(text))
    char_lng_frac = {'japanese': jap_symbols/cjk_symbols,
                     'korean': kor_symbols/cjk_symbols}
    max_char_lng_frac = max(char_lng_frac, key=char_lng_frac.get)
    # check if at least 1/4 of chars are other than chinese,
    # if not -> run chinese tokenizer
    if char_lng_frac[max_char_lng_frac] > lng_frac_par:
        language = max_char_lng_frac
    else:
        language = 'cjk'
    return language


def CJK_tokenization(text, language):
    if language == 'cjk':
        seg = get_ch_tokenizer()
        processed_text = seg.lcut(text, cut_all=False)

    if language == 'japanese':
        mode = jp_tokenizer.Tokenizer.SplitMode.B
        seg = get_jap_tokenizer()
        processed_text = [m.surface()
                               for m in seg.tokenize(str(text), # noqa
                               mode)]

    if language == 'korean':
        seg = get_kor_tokenizer()
        processed_text = seg.nouns(text)
        # this is a "feature" in Korean tokenizer
        if processed_text == []:
            processed_text = [text]

    return processed_text
