import re
from collections import namedtuple

import yamlconf
from hat_trie import Trie

from .token import Token


class Tokenizer:
    """
    Constructs a tokenizaton strategy.
    """
    def tokenize(self, text):
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
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.regex = re.compile('|'.join('(?P<{0}>{1})'.format(name, pattern)
                                         for name, pattern in lexicon))

    def tokenize(self, text):
        return [t for t in self._tokenize(text)]

    def _tokenize(self, text):
        """
        Tokenizes a text

        :Returns:
            A `list` of tokens
        """
        tokens = Trie()

        for i, match in enumerate(self.regex.finditer(text)):
            value = match.group(0)

            try:
                token = tokens[value]
            except KeyError:
                type = match.lastgroup
                token = Token(value, type)
                tokens[value] = token

            yield token
