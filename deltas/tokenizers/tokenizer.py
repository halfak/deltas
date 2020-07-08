import re

import yamlconf

from .token import Token
import pkuseg
from konlpy.tag import Mecab as ko_mecab
import MeCab as jp_mecab


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
            char_lang_count = {'cjk': 1,
                               'japanese': 0.75 + jap_symbols/cjk_symbols,
                               'korean': 0.75 + kor_symbols/cjk_symbols}
            char_lang = max(char_lang_count, key=char_lang_count.get)
            tokenized_text = self._cjk_tokenization(tokenized_text, language=char_lang, token_class=token_class)
        return tokenized_text

    def _cjk_tokenization(self, tokenized_text, language, token_class=None):
        token_class = token_class or Token
        cjk_word_indices = list(filter(lambda x: tokenized_text[x].type == 'cjk_word', range(len(tokenized_text))))

        if language == 'cjk':
            seg = pkuseg.pkuseg()
            for i in cjk_word_indices[::-1]:
                segmented_cjk_token = seg.cut(tokenized_text[i])
                tokenized_text[i:i+1] = [token_class(word, type="cjk_word") for word in segmented_cjk_token]
            return tokenized_text

        if language == 'japanese':
            seg = jp_mecab.Tagger("-Owakati")
            for i in cjk_word_indices[::-1]:
                segmented_cjk_token = seg.parse(tokenized_text[i]).split()
                tokenized_text[i:i+1] = [token_class(word, type="cjk_word") for word in segmented_cjk_token]
            return tokenized_text

        if language == 'korean':
            seg = ko_mecab()
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
