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


class RegexTokenizer(Tokenizer):
    """
    Uses a lexicon of regular expressions and names to tokenize a text string.
    """
    def __init__(self, lexicon, cjk_lexicon=None):
        self.lexicon = lexicon
        self.regex = re.compile('|'.join('(?P<{0}>{1})'.format(name, pattern)
                                         for name, pattern in lexicon))
        if cjk_lexicon is not None:
            self.regex_cjk = re.compile(cjk_lexicon['cjk'])
            self.regex_japanese = re.compile(cjk_lexicon['japanese'])
            self.regex_korean = re.compile(cjk_lexicon['korean'])

    def tokenize(self, text, token_class=None, cjk=False):
        tokenized_text = [t for t in self._tokenize(text, token_class=token_class)]
        if cjk is True:
            cjk_symbols = len(self.regex_cjk.findall(text))
            jap_symbols = len(self.regex_japanese.findall(text))
            kor_symbols = len(self.regex_korean.findall(text))
            char_lang_frac = {'japanese': jap_symbols/cjk_symbols,
                               'korean': kor_symbols/cjk_symbols}
            max_char_lang_frac = max(char_lang_frac, key=char_lang_frac.get)
            # check if at least 1/4 of chars are other than chinese, if not -> run chinese tokenizer
            if char_lang_frac[max_char_lang_frac]>0.25:
                tokenized_text = self._cjk_tokenization(tokenized_text, language=max_char_lang_frac, token_class=token_class)
            else:
                tokenized_text = self._cjk_tokenization(tokenized_text, language='cjk', token_class=token_class)
        return tokenized_text

    def _cjk_tokenization(self, tokenized_text, language, token_class=None):
        token_class = token_class or Token
        cjk_word_indices = list(filter(lambda x: tokenized_text[x].type == 'cjk_word', range(len(tokenized_text))))
        
        if language == 'cjk':
            seg = ch_jieba.initialize()
            for i in cjk_word_indices[::-1]:
                segmented_cjk_token = ','.join(ch_jieba.cut(tokenized_text[i], cut_all=False))
                tokenized_text[i:i+1] = [token_class(word, type="cjk_word") for word in segmented_cjk_token]
            return tokenized_text        

        if language == 'japanese':
            mode = jp_tokenizer.Tokenizer.SplitMode.B
            seg = jp_dictionary.Dictionary().create()
            for i in cjk_word_indices[::-1]:
                segmented_cjk_token = [m.surface() for m in seg.tokenize(str(tokenized_text[i]), mode)]
                tokenized_text[i:i+1] = [token_class(word, type="cjk_word") for word in segmented_cjk_token]
            return tokenized_text

        if language == 'korean':
            seg = ko_okt()
            for i in cjk_word_indices[::-1]:
                segmented_cjk_token = seg.nouns(tokenized_text[i])
                if segmented_cjk_token != []:
                    tokenized_text[i:i+1] = [token_class(word, type="cjk_word") for word in segmented_cjk_token]            
            return tokenized_text

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
