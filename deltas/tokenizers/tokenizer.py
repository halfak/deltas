import re

import yamlconf

from .token import Token

import jieba as ch_jieba
from sudachipy import tokenizer as jp_tokenizer
from sudachipy import dictionary as jp_dictionary
from konlpy.tag import Okt as ko_okt


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
    def __init__(self, tokenizer, *token_segmenters):
        self.tokenizer = tokenizer  # start of the pipeline
        self.token_segmenter = token_segmenters

    def tokenize(self, text):
        tokens = self.tokenizer.tokenize(text)
        for token_segmenter in self.token_segmenter:
            tokens = token_segmenter.segment(tokens)
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
    def segment(self, tokenized_text):
        raise NotImplementedError()


class CJKSegmenter(TokenProcessor):
    """
    Uses a cjk_lexicon to decide which tokenizer should be used
    (Chinese, Japanese or Korean).
    """
    def __init__(self, cjk_lexicon):
        self.regex_cjk = re.compile(cjk_lexicon['cjk'])
        self.regex_japanese = re.compile(cjk_lexicon['japanese'])
        self.regex_korean = re.compile(cjk_lexicon['korean'])

    def segment(self, tokenized_text, token_class=None):
        token_class = token_class or Token
        text = "".join([tok[:] for tok in tokenized_text if tok.type == 'cjk_word']) # noqa
        cjk_symbols = len(self.regex_cjk.findall(text))
        jap_symbols = len(self.regex_japanese.findall(text))
        kor_symbols = len(self.regex_korean.findall(text))
        char_lang_frac = {'japanese': jap_symbols/cjk_symbols,
                          'korean': kor_symbols/cjk_symbols}
        max_char_lang_frac = max(char_lang_frac, key=char_lang_frac.get)
        # check if at least 1/4 of chars are other than chinese,
        # if not -> run chinese tokenizer
        if char_lang_frac[max_char_lang_frac] > 0.25:
            segmented_tokens = self._cjk_segmentation(tokenized_text, language=max_char_lang_frac, token_class=token_class) # noqa
        else:
            segmented_tokens = self._cjk_segmentation(tokenized_text, language='cjk', token_class=token_class) # noqa
        return segmented_tokens

    def _cjk_segmentation(self, tokenized_text, language, token_class=None):
        token_class = token_class or Token
        cjk_word_indices = list(filter(lambda x: tokenized_text[x].type == 'cjk_word', range(len(tokenized_text)))) # noqa

        if language == 'cjk':
            seg = ch_jieba.initialize()
            for i in cjk_word_indices[::-1]:
                segmented_cjk_token = ','.join(ch_jieba.cut(tokenized_text[i], cut_all=False)) # noqa
                tokenized_text[i:i+1] = [token_class(word, type="cjk_word") for word in segmented_cjk_token] # noqa
            return tokenized_text

        if language == 'japanese':
            mode = jp_tokenizer.Tokenizer.SplitMode.B
            seg = jp_dictionary.Dictionary().create()
            for i in cjk_word_indices[::-1]:
                segmented_cjk_token = [m.surface() for m in seg.tokenize(str(tokenized_text[i]), mode)] # noqa
                tokenized_text[i:i+1] = [token_class(word, type="cjk_word") for word in segmented_cjk_token] # noqa
            return tokenized_text

        if language == 'korean':
            seg = ko_okt()
            for i in cjk_word_indices[::-1]:
                segmented_cjk_token = seg.nouns(tokenized_text[i])
                if segmented_cjk_token != []:
                    tokenized_text[i:i+1] = [token_class(word, type="cjk_word") for word in segmented_cjk_token] # noqa
            return tokenized_text
