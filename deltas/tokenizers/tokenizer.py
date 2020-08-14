import re

import yamlconf

from .token import Token

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


class Tokenizer:
    """
    Constructs a tokenizaton strategy.
    """
    def tokenize(self, text, token_class=Token):
        """
        Tokenizes a text.
        """
        raise NotImplementedError()

    @classmethod
    def from_config(cls, config, name, section_key="tokenizers"):
        section = config[section_key][name]
        if 'module' in section:
            return yamlconf.import_module(section['module'])
        else:
            Tokenizer = yamlconf.import_module(section['class'])
            return Tokenizer.from_config(config, name, section_key)


class TokenizerPipeline(Tokenizer):
    def __init__(self, tokenizer, *token_processors):
        self.tokenizer = tokenizer  # start of the pipeline
        self.token_processors = token_processors

    def tokenize(self, text):
        tokens = self.tokenizer.tokenize(text)
        for token_processor in self.token_processors:
            tokens = token_processor.process(tokens)
        return tokens


class RegexTokenizer(Tokenizer):
    """
    Uses a lexicon of regular expressions and names to tokenize a text string.
    """
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.regex = re.compile('|'.join('(?P<{0}>{1})'.format(name, pattern)
                                         for name, pattern in lexicon))

    def tokenize(self, text, token_class=None):
        return [t for t in self._tokenize(text, token_class=token_class)]

    def _tokenize(self, text, token_class=None):
        """
        Tokenizes a text

        :Returns:
            A `list` of tokens
        """
        token_class = token_class or Token
        tokens = {}

        for i, match in enumerate(self.regex.finditer(text)):
            value = match.group(0)

            try:
                token = tokens[value]
            except KeyError:
                type = match.lastgroup
                token = token_class(value, type=type)
                tokens[value] = token

            yield token


class TokenProcessor:
    def process(self, tokenized_text):
        raise NotImplementedError()


class CJKProcessor(TokenProcessor):
    """
    Uses a cjk_lexicon to decide which tokenizer should be used
    (Chinese, Japanese or Korean).
    """
    def __init__(self, cjk_lexicon, lng_frac_par=0.25):
        self.regex_cjk = re.compile(cjk_lexicon['cjk'])
        self.regex_japanese = re.compile(cjk_lexicon['japanese'])
        self.regex_korean = re.compile(cjk_lexicon['korean'])
        self.lng_frac_par = lng_frac_par

    def process(self, tokenized_text, token_class=None):
        token_class = token_class or Token
        language = self._lng_decision(tokenized_text, self.lng_frac_par)
        processed_tokens = self._cjk_processing(tokenized_text,
                                                language=language,
                                                token_class=token_class)
        return processed_tokens

    def _lng_decision(self, tokenized_text, lng_frac_par=0.25):
        text = "".join([tok[:]
                        for tok in tokenized_text
                        if tok.type == 'cjk_word'])
        cjk_symbols = len(self.regex_cjk.findall(text))
        jap_symbols = len(self.regex_japanese.findall(text))
        kor_symbols = len(self.regex_korean.findall(text))
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

    def _cjk_processing(self, tokenized_text, language, token_class=None):
        token_class = token_class or Token
        cjk_word_indices = list(filter(
                                lambda x:
                                tokenized_text[x].type == 'cjk_word',
                                range(len(tokenized_text))))

        if language == 'cjk':
            seg = get_ch_tokenizer()
            for i in cjk_word_indices[::-1]:
                processed_cjk_token = seg.lcut(tokenized_text[i],
                                               cut_all=False)
                tokenized_text[i:i+1] = [token_class(word, type="cjk_word")
                                         for word in processed_cjk_token]
            return tokenized_text

        if language == 'japanese':
            mode = jp_tokenizer.Tokenizer.SplitMode.B
            seg = get_jap_tokenizer()
            for i in cjk_word_indices[::-1]:
                processed_cjk_token = [m.surface()
                                       for m in seg.tokenize(str(tokenized_text[i]), # noqa
                                       mode)]
                tokenized_text[i:i+1] = [token_class(word, type="cjk_word")
                                         for word in processed_cjk_token]
            return tokenized_text

        if language == 'korean':
            seg = get_kor_tokenizer()
            for i in cjk_word_indices[::-1]:
                processed_cjk_token = seg.nouns(tokenized_text[i])
                if processed_cjk_token != []:
                    tokenized_text[i:i+1] = [token_class(word, type="cjk_word")
                                             for word in processed_cjk_token]
            return tokenized_text
